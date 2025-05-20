from django import views
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from apps.core.forms import OperationForm
from apps.core.models import Operation
from apps.core.models.enums import TransactionType


# Create your views here.
def hello(request):
    # return HttpResponse("Hello, World!")
    # mime type
    # return HttpResponse("Hello, World!", content_type='text/plain')
    return HttpResponse("<h1>Hello, World!</h1>", content_type='text/html')


def about_project(request):
    return render(request, 'about_project.html')


def about_core(request):
    return render(request, 'core/about_core.html')


@require_http_methods(['GET', 'POST'])
def operations(request):
    # POST
    if request.method == 'POST':
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        description = request.POST.get('description')
        type = request.POST.get('type')

        # Можна додати валідацію

        Operation.objects.create(
            amount=amount,
            date=date,
            description=description,
            type=type
        )

        return redirect('core:operations')

    # GET
    context = {
        'operations_list': Operation.objects.all(),
        'type_choices': TransactionType
    }
    return render(request, 'core/pages/operations.html', context)


class OperationDetailUpdateView(views.View):
    def get(self, request, pk):
        operation = get_object_or_404(Operation, pk=pk)
        print(operation)
        operation_form = OperationForm(instance=operation)
        context = {
            'operation_form': operation_form,
        }
        return render(request, 'core/pages/operation_detail.html', context)

    def post(self, request, pk):
        pass

