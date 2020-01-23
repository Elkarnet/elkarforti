from django import forms

from .models import FortiGroup, FortiParameters
from django.contrib import admin

class FortiGroupForm(forms.ModelForm):
    class Meta:
        model = FortiGroup
        fields = ['enabled']

class FortiParametersAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FortiParametersAdminForm, self).__init__(*args, **kwargs)
        self.fields['fortiPassword'].widget = forms.PasswordInput()

