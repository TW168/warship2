# report/forms.py

from django import forms
from .models import ReportInput

class ReportForm(forms.ModelForm):
    class Meta:
        model = ReportInput
        fields = ['date', 'lolita_mtd', 'houston_mtd', 'remington_mtd']

