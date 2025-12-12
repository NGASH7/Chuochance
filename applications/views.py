import datetime
import os
import json
from django.urls import reverse
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import ListView, TemplateView
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_list_or_404

from django_filters.views import FilterView

from formtools.wizard.views import SessionWizardView

from bootstrap_modal_forms.generic import BSModalReadView, BSModalUpdateView, BSModalDeleteView

from .forms import PeriodForm, LevelForm, PersonalDetailsForm, FamilyDetailsForm, LevelModalForm
from .models import Level, Period, Application, Ward
from .filters import ApplicationFilter
# Create your views here.


def load_wards(request):
    subcounty_id = request.GET.get('subcounty')
    wards = Ward.objects.filter(subcounty_id=subcounty_id).order_by('name')
    return render(request, 'applications/_ward_dropdown_list_options.html', {'wards': wards})


def period_and_level_settings(request):
    """
    Settings for Current Period and Level allocations
    """
    levels = Level.objects.all()
    current_period = Period.objects.get(year=datetime.date.today().year)
    period_form = PeriodForm(request.POST or None, instance=current_period)
    level_form = LevelForm(request.POST or None)

    if request.method == 'POST':
        if period_form.is_valid():
            period_form.save()
            # level_form.save()
            messages.success(request, 'Details Updated Successfully')
            return redirect(request.META.get('HTTP_REFERER', '/'))

    context = {
        'title': 'Settings',
        'levels': levels,
        'current_period': current_period,
        'period_form': period_form,
        'level_form': level_form,
    }

    return render(request, 'applications/settings_form.html', context)


class ApplicationsListView(FilterView):
    template_name = 'applications/applications_list.html'
    context_object_name = 'applications'
    filterset_class = ApplicationFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_period = Period.objects.get(
            year=datetime.date.today().year)
        context["current_period"] = current_period
        context['title'] = f'Applications List for Year {current_period.year}'
        return context

    def get_queryset(self):
        current_period = Period.objects.get(year=datetime.date.today().year)
        queryset = Application.objects.filter(period=current_period)
        return queryset


class RecommendedListView(FilterView):
    template_name = 'applications/applications_list.html'
    context_object_name = 'applications'
    filterset_class = ApplicationFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_period = Period.objects.get(
            year=datetime.date.today().year)
        context["current_period"] = current_period
        context['title'] = f'Recommended Applications for Year {current_period.year}'
        context["recommended"] = True
        return context

    def get_queryset(self):
        current_period = Period.objects.get(year=datetime.date.today().year)
        queryset = Application.objects.filter(
            period=current_period, recommended=True)
        return queryset


class SuccessfulListView(FilterView):
    template_name = 'applications/applications_list.html'
    context_object_name = 'applications'
    filterset_class = ApplicationFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_period = Period.objects.get(
            year=datetime.date.today().year)
        context["current_period"] = current_period
        context['title'] = f'Successful Applications for Year {current_period.year}'
        context["successful"] = True
        return context

    def get_queryset(self):
        current_period = Period.objects.get(year=datetime.date.today().year)
        queryset = Application.objects.filter(
            period=current_period, award_status='awarded')
        return queryset


class ApplicationView(SessionWizardView):
    """
    Application form to be used
    """
    form_list = [
        ('personal_details', PersonalDetailsForm),
        ('family_details', FamilyDetailsForm)
    ]
    TEMPLATES = {
        'personal_details': 'applications/wizard/personal_details.html',
        'family_details': 'applications/wizard/family_details.html'
    }

    file_storage = FileSystemStorage(location=os.path.join(
        settings.MEDIA_ROOT, 'death_certs_tmp'))

    def get_form(self, step=None, data=None, files=None):
        """
        docstring
        """
        # ''' FILE MANAGEMENT IN THE WIZARD '''
        if step is not None:
            step_files = self.storage.get_step_files(step)
        else:
            step_files = self.storage.current_step_files

        if step_files and files:
            for key, value in step_files.items():
                if files.__contains__(key) and files[key] is not None:
                    step_files[key] = files[key]
        elif files:
            step_files = files

            # ''' END OF FILE MANAGEMENT IN WIZARD '''
        return super(ApplicationView, self).get_form(step, data, step_files)

    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["wizard_steps"] = [
            {
                'step_name': 'personal_details',
                'wizard_title': 'Personal Details',
                'wizard_icon': 'fas fa-users-cog'
            },
            {
                'step_name': 'family_details',
                'wizard_title': 'Family Details',
                'wizard_icon': 'far fa-address-card'
            },
        ]
        return context

    def done(self, form_list, **kwargs):
        """
        docstring
        """
        personal_details_cleaned_data = self.get_cleaned_data_for_step(
            'personal_details')
        family_details_cleaned_data = self.get_cleaned_data_for_step(
            'family_details')
        form_data = {**personal_details_cleaned_data,
                     **family_details_cleaned_data}

        del form_data['select_deceased_parent']

        application = Application(**form_data)

        current_period = Period.objects.get(year=datetime.date.today().year)
        application.period = current_period

        if self.request.user.is_authenticated:
            application.user = self.request.user

        application.save()

        messages.success(self.request, 'Application sent successfully')
        return redirect('/')


class ApplicationDetailView(BSModalReadView):
    """
    View to access all the details regarding a particular applicant
    """
    template_name = 'applications/application_details.html'
    model = Application


def approve_applications(request):
    """
    View to approve and reject applications for the bursary award 
    """
    current_period = Period.objects.get(year=datetime.date.today().year)
    application_ids = json.loads(request.GET.get('application_ids', None))
    applications_to_award = Application.objects.filter(
        pk__in=application_ids, period=current_period)
    other_applications = Application.objects.exclude(
        pk__in=application_ids, period=current_period)

    applications_to_award.update(award_status="awarded")

    for application in other_applications:
        if application.award_status == 'pending':
            application.award_status = 'not_awarded'
            application.save()

    messages.success(request, 'Applications approved successfully')
    return JsonResponse({'url': reverse('successful-list')})


class LevelUpdateView(BSModalUpdateView):
    """
    View responsible for updating a given level
    """
    model = Level
    template_name = 'applications/update_level.html'
    form_class = LevelModalForm
    success_message = 'Success: Level updated successfully'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')


class LevelDeleteView(BSModalDeleteView):
    """
    Confirmation View for deleting a given Level
    """
    model = Level
    template_name = 'applications/delete_level.html'
    success_message = 'Success: Level deleted successfully'

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')


class AnalyticsView(TemplateView):
    """
    View handling the visualization of data
    """
    template_name = 'applications/charts.html'

    def get_context_data(self, **kwargs):
        context = super(AnalyticsView, self).get_context_data(**kwargs)
        context['current_period'] = Period.objects.get(
            year=datetime.date.today().year)
        context["queryset"] = Period.objects.all()
        context['levels'] = Level.objects.all()
        return context


def search_application_by_id(request):
    """
    Search application by ID Number
    """
    id_number = request.GET.get('id_number')
    print(id_number)
    applications = Application.objects.filter(id_number=id_number)
    if not applications:
        messages.error(request, 'Application not found.')
        return redirect('/')

    context = {
        'id_number': id_number,
        'applications': applications,
        'title': 'Search Application'
    }

    return render(request, 'applications/search.html', context)
