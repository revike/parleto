import datetime

from django import forms
from django.forms import CheckboxSelectMultiple

from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):
    GROPING = ('date+', 'date-', 'category+', 'category-', )
    SORT = ('date+', 'date-', 'category+', 'category-', )
    grouping = forms.ChoiceField(choices=[('', '')] + list(zip(GROPING, GROPING)))
    sorting = forms.ChoiceField(choices=[('', '')] + list(zip(GROPING, GROPING)))
    years = range(2000, datetime.date.today().year + 1)
    start_date = forms.DateField(widget=forms.SelectDateWidget(years=years),
                                 required=False)
    end_date = forms.DateField(widget=forms.SelectDateWidget(years=years),
                               required=False)

    category = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Category.objects.all(),
        widget=CheckboxSelectMultiple(),
    )

    class Meta:
        model = Expense
        fields = ('name', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].required = False


class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
