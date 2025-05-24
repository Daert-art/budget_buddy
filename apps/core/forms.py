from django import forms

from apps.core.models import Operation, Tag


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
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сума'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Опис'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'user']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва'}),
        }