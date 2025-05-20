from django import forms

from apps.core.models import Operation


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        # Вибрані поля
        # fields = ['amount', 'date', 'description']
        # Всі поля
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'account', 'tags', 'user', 'category']
        # Налаштування окремих полів
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }