from django import views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from apps.core.forms import OperationForm, TagForm
from apps.core.models import Operation, Tag
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

@login_required
@require_http_methods(['GET', 'POST'])
def operations(request):
    # POST
    user = request.user

    if request.method == 'POST':
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        description = request.POST.get('description')
        type_ = request.POST.get('type')
        tag_id = request.POST.get('tag')
        tag = Tag.objects.filter(id=tag_id).first() if tag_id else None

        # Можна додати валідацію

        Operation.objects.create(
            user=user,
            amount=amount,
            date=date,
            description=description,
            type=type_,
            tag=tag,
        )

        return redirect('core:operations')

    # GET
    context = {
        'operations_list': Operation.objects.filter(user=request.user),
        'type_choices': TransactionType,
        'tags_list': Tag.objects.filter(user=request.user),
    }
    return render(request, 'core/pages/operations.html', context)


class OperationDetailUpdateView(views.View):
    def get(self, request, pk):
        operation = get_object_or_404(Operation, pk=pk)
        print(operation)

        operation_form = OperationForm(instance=operation, prefix='operation') # operation_form
        context = {
            'operation': operation,
            'operation_form': operation_form,
        }
        return render(request, 'core/pages/operation_detail.html', context)

    def post(self, request, pk):
        operation = get_object_or_404(Operation, pk=pk)

        operation_form = OperationForm(request.POST, instance=operation, prefix='operation')


        if 'submit_operation' in request.POST:
            if operation_form.is_valid():
                operation_form.save()
                return redirect('core:operation_detail', pk=operation.pk)
            else:
                print(operation_form.errors)

        context = {
            'operation': operation,
            'operation_form': operation_form,
        }
        return render(request, 'core/pages/operation_detail.html', context)

@login_required
@require_http_methods(['POST'])
def operation_delete(request, pk):
    op = get_object_or_404(Operation, pk=pk, user=request.user)
    op.delete()
    return redirect('core:operations')

# --------------------------------------------------------
# TAGS CRUD
# --------------------------------------------------------

@login_required
@require_http_methods(['GET'])
def tag_list(request):
    tags = Tag.objects.filter(user=request.user)
    return render(request, 'core/pages/tag_list.html', {
        'tags': tags,
    })


@login_required
@require_http_methods(['GET', 'POST'])
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect('core:tag_list')
    else:
        form = TagForm()

    return render(request, 'core/pages/tag_form.html', {
        'form': form,
        'action': 'create',
    })


@login_required
@require_http_methods(['GET', 'POST'])
def tag_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('core:tag_list')
    else:
        form = TagForm(instance=tag)

    return render(request, 'core/pages/tag_form.html', {
        'form': form,
        'action': 'update',
        'tag': tag,
    })


@login_required
@require_http_methods(['POST'])
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk, user=request.user)
    tag.delete()
    return redirect('core:tag_list')
