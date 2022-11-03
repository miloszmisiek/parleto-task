from django import forms
from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):
    category_filter = forms.ModelMultipleChoiceField(queryset=Category.objects.all())
    class Meta:
        model = Expense
        fields = ('name', 'date', 'category_filter',)
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['date'].required = False
        self.fields['category_filter'].required = False
