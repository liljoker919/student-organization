from django.shortcuts import render
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

from .models import Task
from .forms import TaskForm



class TaskListView(ListView):
    """
    Display a list of all Task objects.
    The tasks are made available in the template context as 'tasks'.
    """
    model = Task
    template_name = 'assignments/tasks_list.html'
    context_object_name = 'tasks'



class TaskCreateView(CreateView):
    """
    Display a form to create a new Task object.
    Passes the current logged-in user to the form.
    On successful creation, redirects to the tasks list.
    """
    model = Task
    form_class = TaskForm
    template_name = 'assignments/create_task.html'
    success_url = reverse_lazy('tasks')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # 👈 Pass current user to form
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user  # 👈 Assign the logged-in user
        return super().form_valid(form)




class TaskUpdateView(UpdateView):
    """
    Display a form to update an existing Task object.
    Passes the current logged-in user to the form.
    On successful update, redirects to the tasks list.
    """
    model = Task
    form_class = TaskForm
    template_name = 'assignments/update_task.html'
    
    def get_success_url(self):
        # Redirect to tasks list after update
        return reverse_lazy('tasks')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass current user to form
        return kwargs
    
    

class TaskDeleteView(DeleteView):
    """
    Display a confirmation page to delete an existing Task object.
    On confirmation, deletes the task and redirects to the tasks list.
    """
    model = Task
    success_url = reverse_lazy('tasks')
