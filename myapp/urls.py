from django.urls import path
from myapp import views

urlpatterns = [
    path("register/",views.UserCreationView.as_view()),
    path("category/",views.CategoryListCreateView.as_view()),
    path("category/<int:pk>/",views.CategoryRetrieveUpdateView.as_view()),
    path("transaction/",views.TransactionListCreateView.as_view()),
    path("transaction/<int:pk>/",views.TransactionRetrieveUpdateView.as_view()),
    path("expense/summary/",views.ExpensesummaryView.as_view(),name="expense-summary"),
    
  
]
