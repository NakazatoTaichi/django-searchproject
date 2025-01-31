from django.shortcuts import render

def collection_home(request):
    return render(request, 'home.html')
