from django.views.generic import ListView
from .models import Bug
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')

def bug_form(request):
    return render(request, 'bug_form.html')

def page_not_found(request, exception):
    return render(request, '404.html')


class BugListView(ListView):
    model = Bug
    template_name = 'tracker/bug_list.html'
    context_object_name = 'bugs'

class BugCreateView(CreateView):
    model = Bug
    template_name = 'tracker/bug_form.html'
    fields = ['title', 'description', 'severity', 'status', 'assignee']
    success_url = reverse_lazy('bug-list')