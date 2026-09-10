# Personal Expenses Tracker

A working implementation of the project proposed in *Personal Expenses Tracker*
(Tribhuvan University / Mechi Multiple Campus, BCA). Built with Django
(Python), SQLite, and HTML/CSS/JS templates, matching the tech stack and
use cases from the proposal's Use Case Diagram (Figure 3):

| Use case | Where it lives |
|---|---|
| Login / Register | `/login/`, `/register/` |
| Add Transaction | `/transactions/add/` |
| Edit Transaction | `/transactions/<id>/edit/` |
| Delete Transaction | `/transactions/<id>/delete/` |
| View Summary | `/` (dashboard) |
| Generate Report | `/reports/` (category-wise + monthly charts) |
| Logout | sidebar "Log out" button |

The `Transaction` model matches the ER Diagram (Figure 2): each user has
many transactions, each with a type (income/expense), amount, category,
description, and date.

## Setup

1. **Install dependencies** (Python 3.10+ recommended):
   ```bash
   pip install -r requirements.txt
   ```

2. **Create the database** (SQLite file is created automatically):
   ```bash
   python manage.py migrate
   ```

3. **(Optional) Create an admin account** to browse data at `/admin/`:
   ```bash
   python manage.py createsuperuser
   ```

4. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

5. Open **http://127.0.0.1:8000/** in your browser. You'll land on the
   login page — click "Create an account" to register, then start adding
   income/expense entries.

## Project structure

```
config/             Django project settings & root URLs
tracker/            The app: models, views, forms, URLs, admin
  migrations/        Database schema
templates/tracker/  HTML templates (login, register, dashboard, forms, reports)
static/tracker/      CSS
```

## Notes for your report / viva

- **Frontend**: server-rendered HTML/CSS with vanilla JavaScript (category
  filtering on the add/edit form, Chart.js for the report graphs).
- **Backend**: Python via Django (views.py handles all business logic:
  validation, totals calculation, category/monthly aggregation).
- **Database**: SQLite, accessed through Django's ORM — the `Transaction`
  model is the direct implementation of the ER diagram.
- Passwords are hashed by Django's built-in authentication system (never
  stored in plain text), and every transaction is scoped to `request.user`
  so one user can never see or edit another user's records.
- `DEBUG = True` and `ALLOWED_HOSTS = ['*']` in `config/settings.py` are
  fine for local development/demonstration but should be tightened before
  any real deployment.
