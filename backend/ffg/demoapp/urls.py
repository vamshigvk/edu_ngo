from django.contrib import admin
from django.urls import path, include
from api.views import employee_dashboard_view, mentor_dashboard_view, mentee_dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    # Standalone Dashboard Routes (Completely separate from /api/)
    path('dashboard/emp/', employee_dashboard_view, name='emp-dashboard'),
    path('dashboard/mentor/', mentor_dashboard_view, name='mentor-dashboard'),
    path('dashboard/mentee/', mentee_dashboard_view, name='mentee-dashboard'),
]