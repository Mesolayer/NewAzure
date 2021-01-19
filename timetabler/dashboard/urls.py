from django.urls import path
from . import views

# urls for dashboard pages
urlpatterns = [
    path('daily/', views.daily_dashboard, name='daily-dashboard'),
    path('daily/filter/', views.dashboard_filter_tags, name='dashboard-filter'),
    path('daily/detals/', views.dashboard_show_details, name='dashboard-show-details'),
    path('daily/create/', views.create_task, name='create-task'),
    path('daily/assign-tag/', views.assign_tag, name='assign-tag'),
    path('daily/new-tag/', views.create_tag, name='create-tag'),
    path('daily/complete/', views.complete_task, name='complete-task'),
    path('daily/update/', views.update_task, name='update-task'),
    path('daily/delete/', views.delete_task, name='delete-task'),
]
