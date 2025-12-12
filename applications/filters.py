import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit

from .models import Period, Level, Application, Ward


class ApplicationFilter(django_filters.FilterSet):
    class Meta:
        model = Application
        fields = [
            'level', 'subcounty', 'ward'
        ]

    def __init__(self, *args, **kwargs):
        """
        docstring
        """
        super(ApplicationFilter, self).__init__(*args, **kwargs)

        self.form.fields['ward'].queryset = Ward.objects.none()
        print(self.form.data)
        if 'subcounty' in self.form.data:
            try:
                subcounty_id = int(self.data.get('subcounty'))
                self.form.fields['ward'].queryset = Ward.objects.filter(
                    subcounty_id=subcounty_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset

        self.form.helper = FormHelper()
        self.form.helper.form_tag = False
        self.form.helper.layout = Layout(
            Row(
                Column(Field('level', id='id_x_level')),
                Column(Field('subcounty')),
                Column(Field('ward')),
            ),
            Row(
                Column(
                    Submit('filter', 'Apply Filter'),
                    css_class='mb-4'
                )
            )
        )
