from django.views.generic.list import ListView

from django.db.models import Count
from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, total_amount, summary_per_year_month


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        sort = self.request.GET.get("sort")
        dir = self.request.GET.get("dir")
        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            end_date = form.cleaned_data.get('end_date')
            initial_date = form.cleaned_data.get('initial_date')
            categories = form.cleaned_data.get('category_filter')
            if name:
                queryset = queryset.filter(name__icontains=name)
            if end_date or initial_date:
                if end_date and initial_date:
                    queryset = queryset.filter(date__range=(initial_date, end_date))
                else:
                    if end_date:
                        queryset = queryset.filter(date__lte=end_date)
                    if initial_date:
                        queryset = queryset.filter(date__gte=initial_date)
            if categories:
                queryset = queryset.filter(category__in=categories)
        if sort:
            if sort == "date":
                if dir == "asc":
                    queryset = queryset.order_by('date')
                if dir == "desc":
                    queryset = queryset.order_by('-date')
            if sort == "category":
                if dir == "asc":
                    queryset = queryset.order_by('category')
                if dir == "desc":
                    queryset = queryset.order_by('-category')

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            total_amount=total_amount(queryset),
            summary_per_year_month=summary_per_year_month(queryset),
            sort=sort,
            dir=dir,
            **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        return super().get_context_data(
            object_list=queryset
            .annotate(no_expenses=Count('expense')),
            **kwargs)
