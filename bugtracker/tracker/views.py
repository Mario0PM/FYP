from django.views.generic import ListView
from .models import Bug

class BugListView(ListView):
    model = Bug
    template_name = 'tracker/bug_list.html'
    context_object_name = 'bugs'

from django.views.generic import CreateView
from django.urls import reverse_lazy

class BugCreateView(CreateView):
    model = Bug
    template_name = 'tracker/bug_form.html'
    fields = ['title', 'description', 'severity', 'status', 'assignee']
    success_url = reverse_lazy('bug-list')