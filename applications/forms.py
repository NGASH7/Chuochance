from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, ButtonHolder, Div, HTML
from crispy_forms.bootstrap import Accordion, AccordionGroup

from .models import Period, Level, Application, Ward


class PeriodForm(forms.ModelForm):
    """
    Form used to edit the Period Details
    """
    class Meta:
        model = Period
        fields = [
            'start_date', 'end_date',
            'budget'
        ]

    def __init__(self, *args, **kwargs):
        """
        docstring
        """
        super(PeriodForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(Field('start_date')),
                Column(Field('end_date')),
            ),
            Row(Column(Field('budget'))),
            Submit('save', 'Save Changes')
        )


class LevelForm(forms.ModelForm):
    """
    Form Used to edit levels
    """
    class Meta:
        model = Level
        fields = ['name', 'amount_allocated']

    def __init__(self, *args, **kwargs):
        """
        docstring
        """
        super(LevelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(Field('name')),
                Column(Field('amount_allocated')),
            ),
            Submit('save', 'Save Changes')
        )


class LevelModalForm(BSModalModelForm):
    """
    Modal Form Used to edit levels
    """
    class Meta:
        model = Level
        fields = ['name', 'amount_allocated']

    def __init__(self, *args, **kwargs):
        """
        docstring
        """
        super(LevelModalForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(Field('name')),
                Column(Field('amount_allocated')),
            )
        )


class PersonalDetailsForm(forms.ModelForm):
    """
    Form to hold the personal details of the applicant
    """
    class Meta:
        model = Application
        fields = [
            'full_name', 'id_number',
            'gender', 'level',
            'school_name', 'school_recommendation_letter',
            'admission_number', 'class_of_study',
            'disability_status',
            'disability_registration_number', 'disability_description',
            'subcounty', 'ward',
        ]

        labels = {
            'id_number': 'ID Number (Personal or Guardian\'s)',
            'disability_status': 'Are you a person living with disability?',
            'disability_registration_number': 'Registration Number with the Disability Council',
            'level': 'Current Level of Education',
            'school_name': 'Name of your School',
            'school_recommendation_letter': 'Recommendation letter from your school'
        }

    def __init__(self, *args, **kwargs):
        """
        docstring
        """
        super(PersonalDetailsForm, self).__init__(*args, **kwargs)

        self.fields['ward'].queryset = Ward.objects.none()

        if 'personal_details-subcounty' in self.data:
            try:
                subcounty_id = int(self.data.get('personal_details-subcounty'))
                self.fields['ward'].queryset = Ward.objects.filter(
                    subcounty_id=subcounty_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['ward'].queryset = self.instance.subcounty.ward_set.order_by(
                'name')

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(Field('full_name')),
                Column(Field('id_number')),
            ),
            Row(
                Column(Field('gender')),
                Column(Field('level'))
            ),
            Row(
                Column(Field('school_name')),
                Column(Field('school_recommendation_letter')),
            ),
            Row(
                Column(Field('admission_number')),
                Column(Field('class_of_study')),
            ),
            Row(
                Div(
                    Column(
                        Field('disability_status',
                              css_class="custom-control-input"),
                    ),
                    css_class="custom-control custom-switch custom-switch-md"
                ),
            ),
            Div(
                Row(
                    Column(Field('disability_registration_number')),
                    Column(Field('disability_description'))
                ),
                css_class='disability_additional_details'
            ),
            Row(
                Column(Field('subcounty', id='id_subcounty')),
                Column(Field('ward', id='id_ward')),
            ),
            ButtonHolder(
                HTML(
                    '{% include "applications/wizard/_buttons.html" %}'
                ),
            ),
        )


class FamilyDetailsForm(forms.ModelForm):
    """
    Form to hold the family details of the applicant
    """
    select_deceased_parent = forms.ChoiceField(
        choices=(
            ('father', 'Father'),
            ('mother', 'Mother')
        )
    )

    class Meta:
        model = Application
        fields = [
            'name_of_guardian', 'contact_of_guardian',
            'family_status',
            'death_cert_father', 'death_cert_mother',
        ]
        labels = {
            'contact_of_guardian': 'Contact Number',
            'death_cert_father': 'Father\'s Death Certificate',
            'death_cert_mother': 'Mother\'s Death Certificate'
        }

    def __init__(self, *args, **kwargs):
        """
        docstring
        """
        super(FamilyDetailsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(Field('name_of_guardian')),
                Column(Field('contact_of_guardian', css_class='phone_input')),
            ),
            Row(
                Column(Field('family_status')),
            ),
            Div(
                Row(
                    Div(
                        Column(Field('select_deceased_parent')),
                        css_class="deceased_parent"
                    ),
                    Div(
                        Div(
                            Column(Field('death_cert_father')),
                            css_class="death_cert_father"
                        ),
                        Div(
                            Column(Field('death_cert_mother')),
                            css_class="death_cert_mother"
                        ),
                        css_class='certificates_section'
                    ),
                ),
                css_class='death_certificates'
            ),
            ButtonHolder(
                HTML(
                    '{% include "applications/wizard/_buttons.html" %}'
                ),
            ),
        )
