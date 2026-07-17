from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Todo
from .forms import TodoForm


@login_required
def todo_list(request):
    todos = Todo.objects.filter(user=request.user)
    show = request.GET.get('show', 'all')
    if show == 'pending':
        todos = todos.filter(completed=False)
    elif show == 'completed':
        todos = todos.filter(completed=True)

    context = {
        'todos': todos,
        'show': show,
        'pending_count': Todo.objects.filter(user=request.user, completed=False).count(),
    }
    return render(request, 'todos/todo_list.html', context)


@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Task added.')
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todos/todo_form.html', {'form': form, 'title': 'Add Task'})


@login_required
def todo_update(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated.')
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/todo_form.html', {'form': form, 'title': 'Edit Task'})


@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Task deleted.')
        return redirect('todo_list')
    return render(request, 'todos/todo_confirm_delete.html', {'todo': todo})


@login_required
def todo_toggle(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')
