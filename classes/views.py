from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import StudentClass
from .forms import StudentClassForm


class StudentClassListView(ListView):
    """Displays all class objects."""
    model = StudentClass
    context_object_name = 'classes'
    # template_name = 'classes/class_list.html'


class StudentClassDetailView(DetailView):
    """Displays details of a single class."""
    model = StudentClass
    context_object_name = 'class_obj'
    # template_name = 'classes/class_detail.html'


class StudentClassCreateView(CreateView):
    """Handles creating a new class using a form."""
    model = StudentClass
    form_class = StudentClassForm
    success_url = reverse_lazy('class-list')
    # template_name = 'classes/class_form.html'


# Uncomment this when implement it
# class StudentClassUpdateView(UpdateView):
#     """Handles updating an existing class."""
#     model = StudentClass
#     form_class = StudentClassForm
#     success_url = reverse_lazy('class-list')
#     template_name = 'classes/class_form.html'


class StudentClassDeleteView(DeleteView):
    """Handles deleting a class."""
    model = StudentClass
    success_url = reverse_lazy('class-list')
    # template_name = 'classes/class_confirm_delete.html'
