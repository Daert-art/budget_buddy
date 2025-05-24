from django.urls import path
from django.views.generic import RedirectView

from apps.core import views
from apps.core.views import hello, about_project, about_core, operation_delete

# Оголошення простору імен namespace
app_name = 'core'
urlpatterns = [
    #path('', hello),
    # path('', about_project),
    #path('core/', about_core),
    # about-core адреса має писатись в стилі kebab-case
    path('about/', about_project),
    path('about/core/', about_core),


    path('', RedirectView.as_view(pattern_name='core:operations', permanent=False)),
    path('operations/', views.operations, name='operations'), #core:operations
    path('operations/<int:pk>/',views.OperationDetailUpdateView.as_view(), name='operation_detail'),
    path('operations/<int:pk>/delete/', operation_delete, name='operation_delete'),

    # Теги
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/add/', views.tag_create, name='tag_add'),
    path('tags/<int:pk>/edit/', views.tag_update, name='tag_edit'),
    path('tags/<int:pk>/delete/', views.tag_delete, name='tag_delete'),
]
