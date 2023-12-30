from django.shortcuts import render

def service(request):
    return render(request, 'service/service.html')
