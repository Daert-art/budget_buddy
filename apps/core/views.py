from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def hello(request):
    #return HttpResponse("Hello, World!")
    # mime type
    #return HttpResponse("Hello, World!", content_type='text/plain')
    return HttpResponse("<h1>Hello, World!</h1>", content_type='text/html')

def about_project(request):
    return render(request, 'about_project.html')

def about_core(request):
    return render(request, 'core/about_core.html')

def operations(request):
    return render(request, 'core/pages/operations.html')