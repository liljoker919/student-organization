from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import Task,Notification
from .forms import TaskForm


@login_required
def dashboard(request):
    """
    Display the user dashboard with organized task snapshots:
    - Upcoming tasks (due within 7 days)
    - Overdue tasks 
    - Recently completed tasks
    """
    # Get today's date for filtering
    today = timezone.localdate()
    upcoming_deadline = today + timedelta(days=7)
    recent_completion_period = today - timedelta(days=7)
    
    # Filter tasks for the current user
    user_tasks = Task.objects.filter(user=request.user)
    
    # Upcoming tasks: due within next 7 days and not complete
    upcoming_tasks = user_tasks.filter(
        due_date__lte=upcoming_deadline,
        due_date__gte=today,
        status__in=['todo', 'in_progress']
    ).order_by('due_date', 'priority')
    
    # Overdue tasks: past due date and not complete
    overdue_tasks = user_tasks.filter(
        due_date__lt=today,
        status__in=['todo', 'in_progress']
    ).order_by('due_date')
    
    # Recently completed tasks: completed within last 7 days
    recently_completed = user_tasks.filter(
        status='complete',
        updated_at__date__gte=recent_completion_period
    ).order_by('-updated_at')[:10]  # Limit to 10 most recent
    
    context = {
        'upcoming_tasks': upcoming_tasks,
        'overdue_tasks': overdue_tasks,
        'recently_completed': recently_completed,
        'today': today,
        'upcoming_deadline': upcoming_deadline,
    }
    
    return render(request, 'tasks/dashboard.html', context)



class TaskListView(LoginRequiredMixin,ListView):
    """
    Display a list of all Task objects.
    The tasks are made available in the template context as 'tasks'.
    """
    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'



class TaskCreateView(LoginRequiredMixin,CreateView):
    """
    Display a form to create a new Task object.
    Passes the current logged-in user to the form.
    On successful creation, redirects to the tasks list.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create_task.html'
    success_url = reverse_lazy('tasks')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # 👈 Pass current user to form
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user  # 👈 Assign the logged-in user
        return super().form_valid(form)




class TaskUpdateView(LoginRequiredMixin,UpdateView):
    """
    Display a form to update an existing Task object.
    Passes the current logged-in user to the form.
    On successful update, redirects to the tasks list.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update_task.html'
    
    def get_success_url(self):
        # Redirect to tasks list after update
        return reverse_lazy('tasks')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass current user to form
        return kwargs
    
    

class TaskDeleteView(LoginRequiredMixin,DeleteView):
    """
    Display a confirmation page to delete an existing Task object.
    On confirmation, deletes the task and redirects to the tasks list.
    """
    model = Task
    success_url = reverse_lazy('tasks')



@login_required
def notification_list(request):
    """Display all notifications for the current user."""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tasks/notifications.html', {
        'notifications': notifications
    })



@login_required
def delete_notification(request, pk):
    """Delete a notification by its PK."""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    if request.method == "POST":
        notification.delete()
    return redirect('notifications')