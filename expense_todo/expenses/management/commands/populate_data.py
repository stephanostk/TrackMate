from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from expenses.models import Expense
from todos.models import Todo
from datetime import datetime, timedelta
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Populate sample data for expenses and todos'

    def handle(self, *args, **options):
        # Get or create a user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )

        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created user: testuser'))
        else:
            self.stdout.write(self.style.WARNING('User already exists'))

        # Sample expenses data
        expenses_data = [
            {'title': 'Grocery Shopping', 'category': 'Food', 'amount': 2500, 'days_ago': 0},
            {'title': 'Restaurant Dinner', 'category': 'Food', 'amount': 1200, 'days_ago': 1},
            {'title': 'Fuel', 'category': 'Transport', 'amount': 1500, 'days_ago': 2},
            {'title': 'Cab Ride', 'category': 'Transport', 'amount': 350, 'days_ago': 3},
            {'title': 'Movie Tickets', 'category': 'Entertainment', 'amount': 800, 'days_ago': 4},
            {'title': 'Coffee', 'category': 'Food', 'amount': 150, 'days_ago': 5},
            {'title': 'Gym Membership', 'category': 'Health', 'amount': 2000, 'days_ago': 6},
            {'title': 'Electricity Bill', 'category': 'Bills', 'amount': 3500, 'days_ago': 7},
            {'title': 'New Shoes', 'category': 'Shopping', 'amount': 2000, 'days_ago': 8},
            {'title': 'Pharmacy', 'category': 'Health', 'amount': 800, 'days_ago': 9},
            {'title': 'Internet Bill', 'category': 'Bills', 'amount': 1200, 'days_ago': 10},
            {'title': 'Online Clothes', 'category': 'Shopping', 'amount': 3500, 'days_ago': 11},
            {'title': 'Concert Ticket', 'category': 'Entertainment', 'amount': 2000, 'days_ago': 12},
            {'title': 'Lunch', 'category': 'Food', 'amount': 600, 'days_ago': 13},
            {'title': 'Gas Refill', 'category': 'Transport', 'amount': 2500, 'days_ago': 14},
        ]

        # Create expenses
        for data in expenses_data:
            date = datetime.now().date() - timedelta(days=data['days_ago'])
            expense, created = Expense.objects.get_or_create(
                user=user,
                title=data['title'],
                date=date,
                defaults={
                    'category': data['category'],
                    'amount': Decimal(str(data['amount'])),
                    'notes': f'Sample {data["category"]} expense'
                }
            )
            if created:
                self.stdout.write(f'Created expense: {data["title"]}')

        # Sample todos data
        todos_data = [
            {'title': 'Complete Project Report', 'priority': 'High', 'days_due': 2},
            {'title': 'Pay Monthly Bills', 'priority': 'High', 'days_due': 5},
            {'title': 'Schedule Doctor Appointment', 'priority': 'Medium', 'days_due': 10},
            {'title': 'Buy Groceries', 'priority': 'Medium', 'days_due': 1},
            {'title': 'Call Mom', 'priority': 'Low', 'days_due': 3},
            {'title': 'Review Budget', 'priority': 'High', 'days_due': 7},
            {'title': 'Exercise 30 minutes', 'priority': 'Medium', 'days_due': 0},
            {'title': 'Read a Book Chapter', 'priority': 'Low', 'days_due': 5},
            {'title': 'Clean Room', 'priority': 'Low', 'days_due': 2},
            {'title': 'Attend Meeting at 2 PM', 'priority': 'High', 'days_due': 0},
        ]

        # Create todos
        for data in todos_data:
            due_date = datetime.now().date() + timedelta(days=data['days_due'])
            todo, created = Todo.objects.get_or_create(
                user=user,
                title=data['title'],
                defaults={
                    'priority': data['priority'],
                    'due_date': due_date,
                    'description': f'Sample task for {data["title"]}',
                    'completed': random.choice([True, False])
                }
            )
            if created:
                self.stdout.write(f'Created todo: {data["title"]}')

        self.stdout.write(self.style.SUCCESS('Successfully populated data!'))
        self.stdout.write(self.style.SUCCESS(f'Username: testuser | Password: testpass123'))
