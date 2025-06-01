from django import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST

from apps.core.forms import OperationForm, AccountForm, TagForm, BudgetForm, CategoryForm, RecurringForm
from apps.core.models import Operation, Tag, Account, Budget, Category, Recurring
from apps.core.models.enums import TransactionType


# Create your views here.
def hello(request):
    # return HttpResponse("Hello, World!")
    # mime type
    # return HttpResponse("Hello, World!", content_type='text/plain')
    return HttpResponse("<h1>Hello, World!</h1>", content_type='text/html')


def about_project(request):
    return render(request, 'about_project.html')
# SECURITY 1
#@login_required
def about_core(request):
    return render(request, 'core/about_core.html')


#@login_required
@require_http_methods(['GET', 'POST'])
def operations(request):
    # POST
    user = request.user

    if request.method == 'POST':
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        description = request.POST.get('description')
        type_ = request.POST.get('type')
        category_id = request.POST.get('category')
        category = Category.objects.filter(id=category_id).first() if category_id else None
        tag_id = request.POST.get('tag')
        tag = Tag.objects.filter(id=tag_id).first() if tag_id else None

        # Можна додати валідацію

        Operation.objects.create(
            user=user,
            amount=amount,
            date=date,
            description=description,
            type=type_,
            category=category,
            tag=tag,
        )

        return redirect('core:operations')

    # GET
    context = {
        'operations_list': Operation.objects.filter(user=request.user),
        'type_choices': TransactionType,
        'categories': Category.objects.filter(user=request.user),
        'tags_list': Tag.objects.filter(user=request.user),
        'account': Account.objects.filter(user=request.user).first(),
    }
    return render(request, 'core/pages/operations.html', context)

#SECURITY 2 LoginRequiredMixin має наслідуватися першим
class OperationDetailUpdateView(views.View):
    def get(self, request, pk):
        operation = get_object_or_404(Operation, pk=pk)
        print(operation)

        operation_form = OperationForm(instance=operation, user=request.user)  # operation_form
        context = {
            'operation': operation,
            'operation_form': operation_form,
        }
        return render(request, 'core/pages/operation_detail.html', context)

    def post(self, request, pk):
        operation = get_object_or_404(Operation, pk=pk)

        operation_form = OperationForm(request.POST, instance=operation, user=request.user)  # Передаємо користувача

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


#@login_required
@require_http_methods(['POST'])
def operation_delete(request, pk):
    op = get_object_or_404(Operation, pk=pk, user=request.user)
    op.delete()
    return redirect('core:operations')


class AccountDetailView(views.View):
    def get(self, request, pk):
        account = get_object_or_404(Account, pk=pk, user=request.user)
        account_form = AccountForm(instance=account)
        context = {
            'account': account,
            'operations': account.operations.all(),
            'account_form': account_form,
        }
        return render(request, 'core/pages/account.html', context)

    def post(self, request, pk):
        account = get_object_or_404(Account, pk=pk, user=request.user)
        account_form = AccountForm(request.POST, request.FILES, instance=account)

        if account_form.is_valid():
            account = account_form.save(commit=False)
            account.user = request.user
            account.save()
            return redirect('core:account_detail', pk=account.pk)
        else:
            print("Errors:", account_form.errors)

        context = {
            'account': account,
            'account_form': account_form,
        }
        return render(request, 'core/pages/account.html', context)


# --------------------------------------------------------
# TAGS CRUD
# --------------------------------------------------------

#@login_required
@require_http_methods(['GET'])
def tag_list(request):
    category_id = request.GET.get('category')
    tags = Tag.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)

    if category_id:
        tags = tags.filter(category_id=category_id)

    return render(request, 'core/pages/tag_list.html', {
        'tags': tags,
        'categories': categories,
        'selected_category_id': int(category_id) if category_id else None
    })


#@login_required
@require_http_methods(['GET', 'POST'])
def tag_create(request):
    if request.method == 'POST':
        form = TagForm(request.POST, user=request.user)  # Передаємо користувача
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect('core:tag_list')
    else:
        form = TagForm(user=request.user)

    return render(request, 'core/pages/tag_form.html', {
        'form': form,
        'action': 'create',
    })


#@login_required
@require_http_methods(['GET', 'POST'])
def tag_update(request, pk):
    tag = get_object_or_404(Tag, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag, user=request.user)  # Передаємо користувача
        if form.is_valid():
            form.save()
            return redirect('core:tag_list')
    else:
        form = TagForm(instance=tag, user=request.user)  # Передаємо користувача

    return render(request, 'core/pages/tag_form.html', {
        'form': form,
        'action': 'update',
        'tag': tag,
    })


#@login_required
@require_http_methods(['POST'])
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk, user=request.user)
    tag.delete()
    return redirect('core:tag_list')


# --------------------------------------------------------
# BUDGET CRUD
# --------------------------------------------------------

#@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)

    total_limit = sum(b.limit_amount for b in budgets)
    total_spent = sum(b.spent_amount() for b in budgets)  # ← ВИКЛИК методу
    total_remaining = total_limit - total_spent
    total_percent = (total_spent / total_limit * 100) if total_limit else 0

    return render(request, 'core/pages/budget_list.html', {
        'budgets': budgets,
        'total_limit': total_limit,
        'total_spent': total_spent,
        'total_remaining': total_remaining,
        'total_percent': round(total_percent),
    })


#@login_required
@require_http_methods(['GET', 'POST'])
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST, user=request.user)  # Передаємо користувача
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('core:budget_list')
    else:
        form = BudgetForm(user=request.user)  # Передаємо користувача
    return render(request, 'core/pages/budget_form.html', {'form': form, 'action': 'create'})


#@login_required
@require_http_methods(['GET', 'POST'])
def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget, user=request.user)  # Передаємо користувача
        if form.is_valid():
            form.save()
            return redirect('core:budget_list')
    else:
        form = BudgetForm(instance=budget, user=request.user)  # Передаємо користувача
    return render(request, 'core/pages/budget_form.html', {'form': form, 'action': 'update', 'budget': budget})


#@login_required
@require_POST
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    budget.delete()
    return redirect('core:budget_list')


# Категорії


#@login_required
@require_http_methods(["GET"])
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'core/pages/category_list.html', {'categories': categories})


#@login_required
@require_http_methods(["GET", "POST"])
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('core:category_list')
    else:
        form = CategoryForm()
    return render(request, 'core/pages/category_form.html', {'form': form, 'action': 'create'})


#@login_required
@require_http_methods(["GET", "POST"])
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('core:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'core/pages/category_form.html', {'form': form, 'action': 'update'})


#@login_required
@require_http_methods(["POST"])
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    category.delete()
    return redirect('core:category_list')


# Recurring Operations
#@login_required
def recurring_list(request):
    recurrings = Recurring.objects.filter(user=request.user)
    return render(request, 'core/pages/recurring_list.html', {'recurrings': recurrings})


# @login_required
# @require_http_methods(["GET", "POST"])
# def recurring_create(request):
#     if request.method == 'POST':
#         form = RecurringForm(request.POST)
#         if form.is_valid():
#             recurring = form.save(commit=False)
#             recurring.user = request.user
#             recurring.save()
#             return redirect('core:recurring_list')
#     else:
#         form = RecurringForm()
#     return render(request, 'core/pages/recurring_form.html', {'form': form})

#@login_required
@require_http_methods(["GET", "POST"])
def recurring_create(request):
    if request.method == 'POST':
        print("POST request received")
        print("Is AJAX:", request.headers.get('x-requested-with'))

        form = RecurringForm(request.POST, user=request.user)  # ← user передаємо сюди

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            print("Form valid?", form.is_valid())
            print(form.errors)
            if form.is_valid():
                recurring = form.save(commit=False)
                recurring.user = request.user
                recurring.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': form.errors.as_json()})
        else:
            if form.is_valid():
                recurring = form.save(commit=False)
                recurring.user = request.user
                recurring.save()
                return redirect('core:recurring_list')
    else:
        form = RecurringForm(user=request.user)  # ← ВАЖЛИВО: user передаємо сюди

    return render(request, 'core/pages/recurring_form.html', {'form': form})



#@login_required
@require_http_methods(["GET", "POST"])
def recurring_update(request, pk):
    recurring = get_object_or_404(Recurring, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RecurringForm(request.POST, instance=recurring, user=request.user)  # Передаємо користувача
        if form.is_valid():
            form.save()
            return redirect('core:recurring_list')
    else:
        form = RecurringForm(instance=recurring, user=request.user)  # Передаємо користувача
    return render(request, 'core/pages/recurring_form.html', {'form': form, 'action': 'update'})


#@login_required
@require_POST
def recurring_delete(request, pk):
    recurring = get_object_or_404(Recurring, pk=pk, user=request.user)
    recurring.delete()
    return redirect('core:recurring_list')

# # @csrf_exempt
#@login_required
@require_POST
def operation_form_ajax(request, pk):
    operation = get_object_or_404(Operation, pk=pk, user=request.user)
    form = OperationForm(request.POST, instance=operation, user=request.user)  # Передаємо користувача

    if form.is_valid():
        form.instance.user = request.user
        form.save()
        return JsonResponse({'message': '✅ Операцію оновлено успішно!'})
    else:
        return JsonResponse({
            'message': '❌ Форма містить помилки',
            'errors': form.errors.as_json()
        }, status=400)

def welcome(request):
    # if request.user.is_authenticated:
    #     return redirect('core:operations')
    return render(request, 'core/pages/welcome.html')
