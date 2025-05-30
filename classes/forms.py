from django import forms
from .models import StudentClass

class StudentClassForm(forms.ModelForm):
    # Using Color picker for better UI enhancements.
    color = forms.CharField(
        label='Pick a Color',
        widget=forms.TextInput(attrs={
            'type': 'color',
            'class': 'form-control',
            'placeholder': 'Choose a color'
        }),
        max_length=50
    )

    class Meta:
        model = StudentClass
        fields = ['name', 'color', 'teacher', 'start_time', 'end_time']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter class name'
            }),
            # 'icon': forms.URLInput(attrs={
            #     'class': 'form-control',
            #     'placeholder': 'Enter icon URL'
            # }),
            'teacher': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter teacher name'
            }),
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'Start time'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'End time'
            }),
        }

    # Date field validation.
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_time")
        end = cleaned_data.get("end_time")

        if start and end and start >= end:
            raise forms.ValidationError("Start time must be before end time.")
        
        return cleaned_data