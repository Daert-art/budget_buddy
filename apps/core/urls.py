from django.urls import path
from django.views.generic import RedirectView

from apps.core import views
from apps.core.views import hello, about_project, about_core

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
    path('operations/<int:pk>/',views.OperationDetailUpdateView.as_view(), name='operation_detail')
]
