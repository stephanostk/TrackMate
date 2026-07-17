# TrackMate
Expense tracker and todo list
# Expense & To-Do Tracker (Django)

A simple Django web app combining an **expense tracker** and a **to-do list**, with user accounts so each person's data stays separate.

## Features

- User signup / login / logout
- Dashboard showing total spent, pending tasks, and recent activity
- **Expenses**: add, edit, delete, filter by category, running total
- **To-Do List**: add, edit, delete, mark complete, filter by status, priority levels, due dates
- Clean Bootstrap 5 UI, mobile-friendly
- Django admin panel for managing data directly

## Project Structure

```
expense_todo/
├── config/          # Project settings, main urls, dashboard/signup views
├── expenses/        # Expense app (model, views, forms, urls)
├── todos/           # To-do app (model, views, forms, urls)
├── templates/        # All HTML templates (base.html + app templates)
├── static/           # Static files (empty, ready for CSS/JS if you add any)
├── manage.py
└── requirements.txt
```

## Setup Instructions

1. **Extract the project** and open a terminal in the folder.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```
   Activate it:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations** (creates the SQLite database):
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser** (for admin access, optional):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. Open your browser at **http://127.0.0.1:8000/**
   - Sign up for a new account, or log in
   - Admin panel is at **http://127.0.0.1:8000/admin/**

## How It Works (quick tour)

- `expenses/models.py` — `Expense` model: title, amount, category, date, notes
- `todos/models.py` — `Todo` model: title, description, priority, due date, completed flag
- `config/views.py` — dashboard view (aggregates totals) and signup view
- Each app has its own `views.py`, `forms.py`, and `urls.py` following Django's standard pattern (list → create → update → delete)
- All templates extend `templates/base.html`, which has the navbar and Bootstrap styling

## Ideas to Extend (good for a college project writeup)

- Add charts (e.g. Chart.js) to visualize spending by category
- Add monthly budget limits with alerts
- Export expenses to CSV/PDF
- Add task reminders via email
- Add pagination for large lists

## Tech Stack

- Python 3 / Django 6.0
- SQLite (default, zero setup)
- Bootstrap 5 (via CDN, no npm needed)
