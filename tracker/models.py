from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


INCOME_CATEGORIES = [
    ("salary", "Salary"),
    ("business", "Business"),
    ("freelance", "Freelance"),
    ("investment", "Investment"),
    ("gift", "Gift"),
    ("other_income", "Other Income"),
]

EXPENSE_CATEGORIES = [
    ("food", "Food"),
    ("transport", "Transport"),
    ("housing", "Housing / Rent"),
    ("utilities", "Utilities"),
    ("health", "Health"),
    ("education", "Education"),
    ("entertainment", "Entertainment"),
    ("shopping", "Shopping"),
    ("other_expense", "Other Expense"),
]

CATEGORY_CHOICES = INCOME_CATEGORIES + EXPENSE_CATEGORIES
CATEGORY_LABELS = dict(CATEGORY_CHOICES)

TYPE_CHOICES = [
    ("income", "Income"),
    ("expense", "Expense"),
]


class Transaction(models.Model):
    """
    Mirrors the ER Diagram (Figure 2) in the proposal:
    User (1) --- has ---> (M) Transaction
    Fields: transaction_id (pk, auto), type, amount, date, category, description
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.get_type_display()} - {self.category} - {self.amount}"

    def get_absolute_url(self):
        return reverse("dashboard")

    @property
    def category_label(self):
        return CATEGORY_LABELS.get(self.category, self.category)
