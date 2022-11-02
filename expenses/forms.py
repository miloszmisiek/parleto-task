from django import forms
from .models import Expense

ORDERING_CHOICES = [(0, 'Ascending'), (1, 'Descending')]


class ExpenseSearchForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ('name', 'date',)
        widgets = {
            'date': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['date'].required = False
