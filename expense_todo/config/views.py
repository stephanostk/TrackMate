from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Sum
from expenses.models import Expense
from todos.models import Todo


@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    todos = Todo.objects.filter(user=request.user)

    context = {
        'total_spent': expenses.aggregate(Sum('amount'))['amount__sum'] or 0,
        'expense_count': expenses.count(),
        'recent_expenses': expenses[:5],
        'pending_todos': todos.filter(completed=False)[:5],
        'pending_count': todos.filter(completed=False).count(),
        'completed_count': todos.filter(completed=True).count(),
    }
    return render(request, 'dashboard.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
