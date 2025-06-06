from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import StudentClass
from .forms import StudentClassForm


class StudentClassListView(ListView):
    """Displays all class objects."""
    model = StudentClass
    context_object_name = 'classes'
    template_name = 'classes/classes_list.html'


class StudentClassDetailView(DetailView):
    """Displays details of a single class."""
    model = StudentClass
    context_object_name = 'class_obj'
    template_name = 'classes/class_detail.html'


class StudentClassCreateView(CreateView):
    """Handles creating a new class using a form."""
    model = StudentClass
    form_class = StudentClassForm
    success_url = reverse_lazy('all_classes')
    template_name = 'classes/add_class.html'

    def form_valid(self, form):
        form.instance.user = self.request.user  # ✅ Set the logged-in user
        return super().form_valid(form)

class StudentClassUpdateView(UpdateView):
    """Handles updating an existing class."""
    model = StudentClass
    form_class = StudentClassForm
    template_name = 'classes/edit_class.html'
    

    def get_success_url(self):
        return reverse_lazy('class_detail', kwargs={'pk': self.object.pk})


class StudentClassDeleteView(DeleteView):
    """Handles deleting a class."""
    model = StudentClass
    success_url = reverse_lazy('all_classes')
    template_name = 'classes/confirm_delete.html'
