from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from datetime import datetime, timedelta
import json
from .models import Expense
from .forms import ExpenseForm


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)

    category = request.GET.get('category')
    if category:
        expenses = expenses.filter(category=category)

    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    by_category = (
        Expense.objects.filter(user=request.user)
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    context = {
        'expenses': expenses,
        'total': total,
        'by_category': by_category,
        'categories': Expense.CATEGORY_CHOICES,
        'selected_category': category,
    }
    return render(request, 'expenses/expense_list.html', context)


@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added.')
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Add Expense'})


@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense updated.')
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Edit Expense'})


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Expense deleted.')
        return redirect('expense_list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})


@login_required
@require_GET
def expense_charts(request):
    """Return chart data as JSON for spending patterns"""
    user = request.user
    
    # Category breakdown
    category_data = (
        Expense.objects.filter(user=user)
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    
    categories = [item['category'] for item in category_data]
    amounts = [float(item['total']) for item in category_data]
    
    # Daily spending for last 30 days
    today = datetime.now().date()
    last_30_days = today - timedelta(days=30)
    
    daily_data = {}
    for i in range(30):
        date = today - timedelta(days=i)
        daily_data[date.strftime('%Y-%m-%d')] = 0
    
    expenses = Expense.objects.filter(
        user=user,
        date__gte=last_30_days
    ).values('date').annotate(total=Sum('amount'))
    
    for exp in expenses:
        daily_data[exp['date'].strftime('%Y-%m-%d')] = float(exp['total'])
    
    dates = sorted(daily_data.keys())
    daily_amounts = [daily_data[date] for date in dates]
    
    # Weekly spending
    weekly_data = {}
    for i in range(8):
        week_end = today - timedelta(days=i*7)
        week_start = week_end - timedelta(days=7)
        week_label = f"Week of {week_start.strftime('%b %d')}"
        
        total = Expense.objects.filter(
            user=user,
            date__gte=week_start,
            date__lte=week_end
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        weekly_data[week_label] = float(total)
    
    week_labels = sorted(weekly_data.keys(), reverse=True)
    week_amounts = [weekly_data[label] for label in week_labels]
    
    return JsonResponse({
        'categories': categories,
        'categoryAmounts': amounts,
        'dates': dates,
        'dailyAmounts': daily_amounts,
        'weekLabels': week_labels,
        'weekAmounts': week_amounts,
    })


@login_required
def expense_dashboard(request):
    """Dashboard with charts for spending patterns"""
    expenses = Expense.objects.filter(user=request.user)
    
    total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    by_category = (
        Expense.objects.filter(user=request.user)
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    
    # Average daily spending
    if expenses.exists():
        date_range = (expenses.values('date').order_by('date').first()['date'], 
                     expenses.values('date').order_by('-date').first()['date'])
        days_diff = (date_range[1] - date_range[0]).days + 1
        avg_daily = float(total) / max(days_diff, 1)
    else:
        avg_daily = 0
    
    context = {
        'total': total,
        'by_category': by_category,
        'avg_daily': round(avg_daily, 2),
        'expense_count': expenses.count(),
    }
    return render(request, 'expenses/expense_dashboard.html', context)
