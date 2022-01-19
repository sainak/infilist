from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import Task


def task_view(request):
    search_task = request.GET.get("search")
    tasks = Task.objects.all().filter(deleted=False, completed=False)
    if search_task:
        tasks = tasks.filter(title__icontains=search_task)
    return render(request, "tasks.html", {"tasks": tasks})


def add_task_view(request):
    task_value = request.GET.get("task")
    task = Task(title=task_value)
    if request.user.is_authenticated:
        task.user = request.user
    task.save()
    return HttpResponseRedirect("/tasks/")


def delete_task_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return HttpResponseRedirect("/tasks/")


def complete_task_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.completed = True
    task.save()
    return HttpResponseRedirect("/tasks/")
