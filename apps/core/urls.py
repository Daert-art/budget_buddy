from django.urls import path
from django.views.generic import RedirectView

from apps.core import views
from apps.core.views import hello, about_project, about_core

# Оголошення простору імен namespace
app_name = 'core'
urlpatterns = [
    # path('', hello),
    # path('', about_project),
    # path('core/', about_core),
    # about-core адреса має писатись в стилі kebab-case
    path('about/', about_project),
    path('about/core/', about_core),

    path('', RedirectView.as_view(pattern_name='core:operations', permanent=False)),
    path('operations/', views.operations, name='operations'),  # core:operations
    path('operations/<int:pk>/', views.OperationDetailUpdateView.as_view(), name='operation_detail'),
    path('operations/<int:pk>/delete/', views.operation_delete, name='operation_delete'),

    # Теги
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/create/', views.tag_create, name='tag_create'),
    path('tags/<int:pk>/update/', views.tag_update, name='tag_update'),
    path('tags/<int:pk>/delete/', views.tag_delete, name='tag_delete'),
    # Акаунти
    path('account/<int:pk>/', views.AccountDetailView.as_view(), name='account_detail'),

    # Бюджети
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/create/', views.budget_create, name='budget_create'),
    path('budgets/<int:pk>/edit/', views.budget_update, name='budget_update'),
    path('budgets/<int:pk>/delete/', views.budget_delete, name='budget_delete'),

    # Категорії
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Повторювані операції
    path('recurrings/', views.recurring_list, name='recurring_list'),
    path('recurrings/create/', views.recurring_create, name='recurring_create'),
    path('recurrings/<int:pk>/update/', views.recurring_update, name='recurring_update'),
    path('recurrings/<int:pk>/delete/', views.recurring_delete, name='recurring_delete'),
]
