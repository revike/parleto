from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .forms import ExpenseSearchForm, CategoryEditForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_year_month, \
    total_amount, total_for_categories


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)

        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            if name:
                queryset = queryset.filter(name__icontains=name)

            categories = form.cleaned_data['category']
            if categories:
                filter_category = Q()
                for category in categories:
                    filter_category |= Q(category=category.id)
                queryset = queryset.filter(filter_category)

            grouping = form.cleaned_data['grouping']
            if grouping == 'date+' or grouping == 'date-':
                if grouping[-1] == '+':
                    queryset = queryset.order_by(grouping[:-1])
                elif grouping[-1] == '-':
                    queryset = queryset.order_by(f'-{grouping[:-1]}')
            elif grouping == 'category+' or grouping == 'category-':
                if grouping[-1] == '+':
                    queryset = queryset.order_by(f'{grouping[:-1]}__name')
                elif grouping[-1] == '-':
                    queryset = queryset.order_by(f'-{grouping[:-1]}__name')

            sorting = form.cleaned_data['sorting']
            if sorting == 'date+' or sorting == 'date-':
                if sorting[-1] == '+':
                    queryset = queryset.order_by(sorting[:-1])
                elif sorting[-1] == '-':
                    queryset = queryset.order_by(f'-{sorting[:-1]}')
            elif sorting == 'category+' or sorting == 'category-':
                if sorting[-1] == '+':
                    queryset = queryset.order_by(f'{sorting[:-1]}__name')
                elif sorting[-1] == '-':
                    queryset = queryset.order_by(f'-{sorting[:-1]}__name')

            start_date = form.cleaned_data['start_date']
            if start_date:
                queryset = queryset.filter(date__gte=start_date)

            end_date = form.cleaned_data['end_date']
            if end_date:
                queryset = queryset.filter(date__lte=end_date)

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            summary_per_year_month=summary_per_year_month(queryset),
            amount=total_amount(queryset),
            **kwargs)


class CategoryListView(ListView):
    model = Category
    template_name = 'expenses/category_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = Expense.objects.all()
        categories = self.model.objects.all()
        return super().get_context_data(
            expenses=total_for_categories(categories, queryset),
        )


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'expenses/category_create.html'
    success_url = reverse_lazy('expenses:expense-list')
    form_class = CategoryEditForm


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'expenses/category_create.html'
    success_url = reverse_lazy('expenses:categories')
    form_class = CategoryEditForm


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expenses:categories')
