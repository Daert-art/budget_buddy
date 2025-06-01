from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve

EXEMPT_URLS = [
    'login',
    'users:logout',
    'users:register',
    'admin:login',
    'admin:logout',
    'admin:index',

    'core:about_project',
    'core:welcome',
    'core:home',
]

class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response



    def __call__(self, request):
       resolver_match = resolve(request.path)
       # view_name включає namespace, наприклад 'core:operations'
       view_name = resolver_match.view_name

       if view_name in EXEMPT_URLS:
              return self.get_response(request)

       if not request.user.is_authenticated:
           return redirect(f'{settings.LOGIN_URL}?next={request.path}')

       return self.get_response(request)



class RoleRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            resolver_match = resolve(request.path)
            url_name = resolver_match.url_name

            # if url_name == 'operations' and request.user.role != 'user':
            #     return redirect('core:about_project')
            if url_name == 'operations' and request.user.role == 'user':
                return self.get_response(request)
            elif url_name == 'users' and request.user.role != 'admin':
                return redirect('core:about_project')

        return self.get_response(request)
