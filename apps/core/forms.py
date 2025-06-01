from django import forms
from apps.core.models import Operation, Account, Tag, Budget, Category, Recurring


class OperationForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['tag'].queryset = Tag.objects.filter(user=user)
            self.fields['category'].queryset = Category.objects.filter(user=user)

    class Meta:
        model = Operation
        exclude = ['created_at', 'updated_at', 'account', 'user']
        labels = {
            'amount': 'Сума',
            'date': 'Дата',
            'description': 'Опис',
            'type': 'Тип операції',
            'tag': 'Тег',
            'category': 'Категорія',
            'is_recurring': 'Повторювана операція',
            'recurring_frequency': 'Частота повторення',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сума'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Опис'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'tag': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'recurring_frequency': forms.Select(attrs={'class': 'form-select'}),
        }


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        exclude = ['created_at', 'updated_at', 'user']
        labels = {
            'name': 'Назва',
            'balance': 'Баланс',
            'currency': 'Валюта',
            'image': 'Зображення',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Баланс'}),
            'currency': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }


class TagForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)

    class Meta:
        model = Tag
        fields = ['name', 'category']
        labels = {
            'name': 'Назва тега',
            'category': 'Категорія',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва тега'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }


class BudgetForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)

    class Meta:
        model = Budget
        exclude = ['created_at', 'updated_at', 'user']
        labels = {
            'limit_amount': 'Ліміт',
            'period_start': 'Початок періоду',
            'period_end': 'Кінець періоду',
            'category': 'Категорія',
        }
        widgets = {
            'limit_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'period_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'period_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        labels = {
            'name': 'Назва категорії',
            'type': 'Тип категорії',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Назва категорії'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
        }


class RecurringForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['account'].queryset = Account.objects.filter(user=user)
            self.fields['category'].queryset = Category.objects.filter(user=user)

    class Meta:
        model = Recurring
        fields = ['amount', 'description', 'type', 'frequency', 'next_date', 'account', 'category']
        labels = {
            'amount': 'Сума',
            'description': 'Опис',
            'type': 'Тип операції',
            'frequency': 'Частота',
            'next_date': 'Наступна дата',
            'account': 'Рахунок',
            'category': 'Категорія',
        }
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'next_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'account': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
