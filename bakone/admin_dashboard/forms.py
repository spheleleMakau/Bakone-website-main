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

    def clean_file(self):
        return self.cleaned_data.get('file', False)


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']
        labels = {
            'name': 'New Folder Name',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if Department.objects.filter(name__iexact=name).exists():
            raise ValidationError('A folder with that name already exists.')
        return name


class DocumentMoveForm(forms.Form):
    target_department = forms.ModelChoiceField(
        queryset=Department.objects.none(),
        required=False,
        label='Move to existing folder'
    )
    new_department = forms.CharField(max_length=100, required=False, label='Or create a new folder')

    def __init__(self, *args, **kwargs):
        current_department = kwargs.pop('current_department', None)
        super().__init__(*args, **kwargs)
        queryset = Department.objects.all().order_by('name')
        if current_department:
            queryset = queryset.exclude(pk=current_department.pk)
        self.fields['target_department'].queryset = queryset
        self.fields['target_department'].empty_label = 'Select destination folder'

    def clean(self):
        cleaned_data = super().clean()
        target_department = cleaned_data.get('target_department')
        new_department = cleaned_data.get('new_department')
        if not target_department and not new_department:
            raise ValidationError('Please choose an existing folder or enter a new one.')
        if new_department and Department.objects.filter(name__iexact=new_department.strip()).exists():
            raise ValidationError('A folder with that name already exists.')
        return cleaned_data
