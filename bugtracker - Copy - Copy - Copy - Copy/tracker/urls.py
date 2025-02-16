from django.urls import path
from .views import BugListView

urlpatterns = [
    path('bugs/', BugListView.as_view(), name='bug-list'),
]
