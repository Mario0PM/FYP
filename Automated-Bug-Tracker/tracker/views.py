import json
import tempfile
import autopep8
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Bug, User, STATUS_CHOICES
from .forms import BugForm, UserForm
from datetime import datetime

User = get_user_model()

class BugListView(ListView):
    """Displays a list of reported bugs."""
    model = Bug
    template_name = 'bug_management.html'
    context_object_name = 'bugs'

    def get_queryset(self):
        return Bug.objects.only("title", "severity", "status", "reporter", "assignee", "created_at").order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = datetime.now().year
        return context

class BugCreateView(LoginRequiredMixin, CreateView):
    """Handles the creation of new bugs and assigns the logged-in user as the reporter."""
    model = Bug
    form_class = BugForm
    template_name = 'bug_management.html'
    success_url = reverse_lazy('bug-list')

    def form_valid(self, form):
        """Automatically set the reporter to the logged-in user before saving."""
        form.instance.reporter = self.request.user
        return super().form_valid(form)

class BugUpdateView(UpdateView):
    """Handles the updating of bug reports."""
    model = Bug
    form_class = BugForm
    template_name = 'bug_management.html'
    success_url = reverse_lazy('bug-list')

    def get_context_data(self, **kwargs):
        """Pass users and selected bug to the template."""
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()  # Pass all users for assignment
        context['selected_bug'] = self.object if hasattr(self, 'object') else None
        return context

@login_required
def bug_delete(request, pk):
    """Handles the deletion of bug reports."""
    bug = get_object_or_404(Bug, pk=pk)
    bug.delete()
    return redirect('bug-list')

@csrf_protect
def homepage_view(request):
    """Homepage view displaying only Open and In Progress bugs."""
    bugs = Bug.objects.filter(status__in=[choice[0] for choice in STATUS_CHOICES if choice[0] in ["Open", "In Progress"]]).order_by('-created_at')
    return render(request, "homepage.html", {"bugs": bugs})

def login_view(request):
    """Handles user login authentication."""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})
    return render(request, "login.html")

def logout_view(request):
    """Handles user logout."""
    logout(request)
    return redirect('login')

def assign_user_to_group(user, role):
    """Assigns a user to a specific group based on their role."""
    try:
        group = Group.objects.get(name=role)
        user.groups.add(group)
        user.save()
    except Group.DoesNotExist:
        pass

@login_required
def user_management_view(request):
    """Handles the user management view."""
    users = User.objects.all()
    return render(request, 'user_management.html', {'users': users})

@login_required
def user_create_view(request):
    """Handles the creation of new users."""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-management')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})

@login_required
def user_update_view(request, pk):
    """Handles the updating of existing users."""
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-management')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

@login_required
def user_delete_view(request, pk):
    """Handles the deletion of users."""
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user-management')
    return render(request, 'user_confirm_delete.html', {'user': user})

@login_required
def user_area(request):
    """Handles the user area view."""
    return render(request, 'user_area.html')

@login_required
def user_area_view(request):
    """Handles the user area view."""
    assigned_bugs = Bug.objects.filter(assignee=request.user)
    return render(request, 'user_area.html', {'assigned_bugs': assigned_bugs})

@login_required
def auto_fix_view(request, pk):
    """Fixes the provided Python code using autopep8."""
    bug = get_object_or_404(Bug, pk=pk)

    if request.method == "POST":
        code_input = request.POST.get('code_input', '').strip()

        if not code_input:
            return JsonResponse({"error": "No code provided"}, status=400)

        try:
            fixed_code = autopep8.fix_code(code_input)
            
            # Format the output nicely
            return render(request, "auto_fix_result.html", {"fixed_code": fixed_code})

        except Exception as e:
            return JsonResponse({"error": f"Error fixing code: {str(e)}"}, status=500)

    return render(request, "user_area.html", {"bug": bug})

