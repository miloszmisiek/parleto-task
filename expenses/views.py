from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category


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
            date = form.cleaned_data.get('date')
            if name:
                queryset = queryset.filter(name__icontains=name)
            if date:
                queryset = queryset.filter(date=date)

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
            sort=sort,
            dir=dir,
            **kwargs)


class CategoryListView(ListView):
    model = Category
    paginate_by = 5
