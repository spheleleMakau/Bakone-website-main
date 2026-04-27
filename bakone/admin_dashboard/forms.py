from django import forms
from .models import CompanyDocument

from django.core.exceptions import ValidationError
import os


from .models import Department

class CompanyDocumentForm(forms.ModelForm):
    new_department = forms.CharField(max_length=100, required=False, label="Or create new folder (department)")

    class Meta:
        model = CompanyDocument
        fields = ['title', 'department', 'new_department', 'file']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['department'].required = False
        self.fields['department'].empty_label = 'Select existing folder (department)'

    def clean(self):
        cleaned_data = super().clean()
        department = cleaned_data.get('department')
        new_department = cleaned_data.get('new_department')
        from .models import Department
        if not department and not new_department:
            raise ValidationError('Please select a folder or create a new one.')
        if new_department:
            if Department.objects.filter(name__iexact=new_department.strip()).exists():
                raise ValidationError(f'A folder named "{new_department}" already exists.')
        return cleaned_data

    # No file type restriction, allow any file
    def clean_file(self):
        return self.cleaned_data.get('file', False)
