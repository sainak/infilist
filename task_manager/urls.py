from django.contrib import admin
from django.urls import path

from tasks import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("tasks/", views.task_view),
    path("add_task/", views.add_task_view),
    path("delete_task/<int:pk>/", views.delete_task_view),
    path("complete_task/<int:pk>/", views.complete_task_view),
    path("start_over/", views.start_over_view),
]
