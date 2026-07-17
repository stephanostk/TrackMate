from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('dashboard/', views.expense_dashboard, name='expense_dashboard'),
    path('api/charts/', views.expense_charts, name='expense_charts'),
    path('add/', views.expense_create, name='expense_create'),
    path('<int:pk>/edit/', views.expense_update, name='expense_update'),
    path('<int:pk>/delete/', views.expense_delete, name='expense_delete'),
]
