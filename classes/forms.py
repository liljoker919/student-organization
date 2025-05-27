from django import forms
from .models import StudentClass

class StudentClassForm(forms.ModelForm):
    # Using Color picker for better Ui enhacements.
    color = forms.CharField(
        label='Pick a Color',
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'form-control',
        }),
        max_length=50
    )

    # All the related fields.
    class Meta:
        model = StudentClass
        fields = ['name', 'color', 'icon', 'teacher', 'start_time', 'end_time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.URLInput(attrs={'class': 'form-control'}),
            'teacher': forms.TextInput(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }

    # Date field validation.
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_time")
        end = cleaned_data.get("end_time")

        if start and end and start >= end:
            raise forms.ValidationError("Start time must be before end time.")
