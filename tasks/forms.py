from django import forms
from django.utils import timezone
from .models import Task
from classes.models import StudentClass


class TaskForm(forms.ModelForm):
    task_type = forms.ChoiceField(
        choices=Task.TASK_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='assignment',
        label='Task Type'
    )

    due_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': timezone.localdate().strftime('%Y-%m-%d')
        }),
        initial=timezone.localdate,
        label='Due Date'
    )

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Task Name',
        required=True
    )

    student_class = forms.ModelChoiceField(
        queryset=StudentClass.objects.none(),  # will be set in __init__
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Class'
    )

    priority = forms.ChoiceField(
        choices=Task.PRIORITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Priority'
    )

    status = forms.ChoiceField(
        choices=Task.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Status'
    )

    class Meta:
        model = Task
        fields = ['task_type', 'name', 'student_class', 'due_date', 'priority', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter student_class queryset by user.And make sure the current user is passed to the form from the view.
        if user:
            self.fields['student_class'].queryset = StudentClass.objects.filter(user=user)

        # Determine current task_type from initial data or posted data
        task_type_value = self.initial.get('task_type') or self.data.get('task_type') or 'assignment'
        self.adjust_status_choices(task_type_value)

        # Add bootstrap classes to radio labels (optional enhancement)
        self.fields['task_type'].widget.attrs.update({'class': 'form-check-input'})

    def adjust_status_choices(self, task_type):
        if task_type == 'test':
            self.fields['status'].choices = [
                choice for choice in Task.STATUS_CHOICES if choice[0] in ['todo', 'complete']
            ]
        else:
            self.fields['status'].choices = Task.STATUS_CHOICES
