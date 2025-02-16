from django.contrib import admin
from django.urls import path, include
from tracker import views
from tracker.views import BugListView, BugCreateView, BugUpdateView, bug_delete, login_view, homepage_view

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Authentication
    path('', login_view, name='login'),  # Default route for login
    path('login/', login_view, name='login'),

    # Homepage
    path('homepage/', homepage_view, name='homepage'),

    # Bug management
    path('bugs/', BugListView.as_view(), name='bug-list'),
    path('bug/create/', BugCreateView.as_view(), name='bug-create'),
    path('bug/<int:pk>/update/', BugUpdateView.as_view(), name='bug-update'),
    path('bug/<int:pk>/delete/', bug_delete, name='bug-delete'),

    # User management
    path('user-management/', views.user_management_view, name='user-management'),
    path('user/create/', views.user_create_view, name='user-create'),  
    path('user/<int:pk>/update/', views.user_update_view, name='user-update'),  
    path('user/<int:pk>/delete/', views.user_delete_view, name='user-delete'),  

    # Logout
    path('logout/', views.logout_view, name='logout'),

    # Automation
    path('my-area/', views.user_area_view, name='my-area'),  # Update this line
    path('auto-fix/<int:pk>/', views.auto_fix_view, name='auto_fix'),  # Add this line
]