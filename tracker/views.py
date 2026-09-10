import calendar
import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import RegisterForm, TransactionForm
from .models import CATEGORY_LABELS, EXPENSE_CATEGORIES, INCOME_CATEGORIES, Transaction


# ---------- Use Case 1: Login / Logout ----------

class TrackerLoginView(LoginView):
    template_name = "tracker/login.html"
    redirect_authenticated_user = True


class TrackerLogoutView(LogoutView):
    next_page = reverse_lazy("login")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully. Welcome!")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "tracker/register.html", {"form": form})


# ---------- Use Case 6: View Summary (Dashboard) ----------

@login_required
def dashboard_view(request):
    transactions = Transaction.objects.filter(user=request.user)

    totals = transactions.aggregate(
        total_income=Sum("amount", filter=Q(type="income")),
        total_expense=Sum("amount", filter=Q(type="expense")),
    )
    total_income = totals["total_income"] or Decimal("0")
    total_expense = totals["total_expense"] or Decimal("0")
    balance = total_income - total_expense

    recent_transactions = transactions[:8]

    context = {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "recent_transactions": recent_transactions,
        "transaction_count": transactions.count(),
    }
    return render(request, "tracker/dashboard.html", context)


# ---------- Use Case 2 & 3: Add / Edit Transaction ----------

@login_required
def transaction_list_view(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, "tracker/transaction_list.html", {"transactions": transactions})


@login_required
def transaction_create_view(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, "Transaction added successfully.")
            return redirect("dashboard")
    else:
        form = TransactionForm(initial={"date": timezone.now().date()})
    context = {
        "form": form,
        "title": "Add Transaction",
        "income_categories": json.dumps(INCOME_CATEGORIES),
        "expense_categories": json.dumps(EXPENSE_CATEGORIES),
    }
    return render(request, "tracker/transaction_form.html", context)


@login_required
def transaction_update_view(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated successfully.")
            return redirect("dashboard")
    else:
        form = TransactionForm(instance=transaction)
    context = {
        "form": form,
        "title": "Edit Transaction",
        "income_categories": json.dumps(INCOME_CATEGORIES),
        "expense_categories": json.dumps(EXPENSE_CATEGORIES),
    }
    return render(request, "tracker/transaction_form.html", context)


# ---------- Use Case 4: Delete Transaction ----------

@login_required
def transaction_delete_view(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        transaction.delete()
        messages.success(request, "Transaction deleted.")
        return redirect("dashboard")
    return render(request, "tracker/transaction_confirm_delete.html", {"transaction": transaction})


# ---------- Use Case 7: Generate Report (category-wise / monthly) ----------

@login_required
def reports_view(request):
    transactions = Transaction.objects.filter(user=request.user)

    # Category-wise breakdown (expenses)
    expense_by_category = (
        transactions.filter(type="expense")
        .values("category")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )
    expense_labels = [CATEGORY_LABELS.get(row["category"], row["category"]) for row in expense_by_category]
    expense_values = [float(row["total"]) for row in expense_by_category]

    income_by_category = (
        transactions.filter(type="income")
        .values("category")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )
    income_labels = [CATEGORY_LABELS.get(row["category"], row["category"]) for row in income_by_category]
    income_values = [float(row["total"]) for row in income_by_category]

    # Monthly summary (income vs expense per month)
    monthly = {}
    for t in transactions:
        key = (t.date.year, t.date.month)
        if key not in monthly:
            monthly[key] = {"income": Decimal("0"), "expense": Decimal("0")}
        monthly[key][t.type] += t.amount

    sorted_keys = sorted(monthly.keys())
    month_labels = [f"{calendar.month_abbr[m]} {y}" for (y, m) in sorted_keys]
    month_income = [float(monthly[k]["income"]) for k in sorted_keys]
    month_expense = [float(monthly[k]["expense"]) for k in sorted_keys]

    context = {
        "expense_labels": json.dumps(expense_labels),
        "expense_values": json.dumps(expense_values),
        "income_labels": json.dumps(income_labels),
        "income_values": json.dumps(income_values),
        "month_labels": json.dumps(month_labels),
        "month_income": json.dumps(month_income),
        "month_expense": json.dumps(month_expense),
        "has_data": transactions.exists(),
    }
    return render(request, "tracker/reports.html", context)


def category_json_view(request):
    """Helper endpoint the Add/Edit form JS uses to filter category options
    based on the selected type (income vs expense)."""
    return JsonResponse({
        "income": INCOME_CATEGORIES,
        "expense": EXPENSE_CATEGORIES,
    })
