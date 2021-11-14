from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import path, reverse_lazy
from .models import Expense
from .views import ExpenseListView, CategoryListView, CategoryCreateView, \
    CategoryUpdateView, CategoryDeleteView

urlpatterns = [
    path('expense/list/',
         ExpenseListView.as_view(),
         name='expense-list'),
    path('expense/create/',
         CreateView.as_view(
            model=Expense,
            fields='__all__',
            success_url=reverse_lazy('expenses:expense-list')
         ),
         name='expense-create'),
    path('expense/<int:pk>/edit/',
         UpdateView.as_view(
            model=Expense,
            fields='__all__',
            success_url=reverse_lazy('expenses:expense-list')
         ),
         name='expense-edit'),
    path('expense/<int:pk>/delete/',
         DeleteView.as_view(
             model=Expense,
             success_url=reverse_lazy('expenses:expense-list')
         ),
         name='expense-delete'),

    path('expense/categories/', CategoryListView.as_view(), name='categories'),
    path('expense/category_add/', CategoryCreateView.as_view(), name='category_add'),
    path('expense/category_update/<int:pk>/',
         CategoryUpdateView.as_view(), name='category_update'),
    path('expense/category_dalete/<int:pk>/',
         CategoryDeleteView.as_view(), name='category_delete'),
]
