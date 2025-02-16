from django.urls import path
from .views import BugListView, BugCreateView, BugUpdateView, bug_delete, create_bug_view

urlpatterns = [
    path('bugs/', BugListView.as_view(), name='bug-list'),
    path('bug/create/', BugCreateView.as_view(), name='bug-create'),
    path('bug/<int:pk>/update/', BugUpdateView.as_view(), name='bug-update'),
    path('bug/<int:pk>/delete/', bug_delete, name='bug-delete'),
    path('create_bug/', create_bug_view, name='create_bug'),
]
