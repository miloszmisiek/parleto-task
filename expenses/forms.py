from django import forms
from .models import Expense, Category


class ExpenseSearchForm(forms.ModelForm):
    category_filter = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
        queryset=Category.objects.all())
    initial_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(
        widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Expense
        fields = ('name', 'initial_date', 'end_date', 'category_filter')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['initial_date'].required = False
        self.fields['end_date'].required = False
        self.fields['category_filter'].required = False
        
        self.fields['initial_date'].label = 'From:'
        self.fields['end_date'].label = 'To:'
        self.fields['category_filter'].label = 'Select Categories:'

