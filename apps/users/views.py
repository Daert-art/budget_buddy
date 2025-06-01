from django import views
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from apps.users.forms import CustomUserCreationForm


# Create your views here.
class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    #success_url = reverse_lazy('login')
    success_url = reverse_lazy('core:welcome')

User = get_user_model()

class UsersListView(views.View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'users/users.html', {'users': users})

    def post(self, request):
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        user = User.objects.get(id=user_id)
        user.role = new_role
        user.save()
        return redirect('users:users')