from django import forms
from .models import Report

class ReportUploadForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = ["title", "file"]