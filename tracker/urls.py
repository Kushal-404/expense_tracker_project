from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("register/", views.register_view, name="register"),
    path("login/", views.TrackerLoginView.as_view(), name="login"),
    path("logout/", views.TrackerLogoutView.as_view(), name="logout"),

    path("transactions/", views.transaction_list_view, name="transaction_list"),
    path("transactions/add/", views.transaction_create_view, name="transaction_add"),
    path("transactions/<int:pk>/edit/", views.transaction_update_view, name="transaction_edit"),
    path("transactions/<int:pk>/delete/", views.transaction_delete_view, name="transaction_delete"),

    path("reports/", views.reports_view, name="reports"),
    path("api/categories/", views.category_json_view, name="category_json"),
]
