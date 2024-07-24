from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import TaskForm
from .models import Task


@login_required(login_url="login")
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.creator = request.user
            task.owner = request.user
            task.save()
            return redirect('list_tasks')
    else:
        form = TaskForm()
    return render(request, 'task_management/create_task.html', {'form': form})


@login_required(login_url="login")
def list_tasks(request):
    tasks_created = Task.objects.filter(creator=request.user)
    tasks_owned_incomplete = Task.objects.filter(owner=request.user, completed=False)
    tasks_owned_complete = Task.objects.filter(owner=request.user, completed=True)
    return render(request, 'task_management/list_tasks.html',
                  {"tasks_created": tasks_created, "tasks_owned_incomplete": tasks_owned_incomplete,
                   "tasks_owned_complete": tasks_owned_complete})


@login_required(login_url="login")
def edit_task(request, task_id):
    """Users can only edit tasks if they are the creators of them"""
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('list_tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_management/edit_task.html', {'form': form, 'task': task})


@login_required(login_url="login")
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('list_tasks')


@login_required(login_url="login")
def mark_task_complete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = True
    task.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url="login")
def mark_task_incomplete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = False
    task.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', 'home'))
