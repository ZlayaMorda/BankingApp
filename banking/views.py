from django.shortcuts import render


def home(request):
    print('HELOOOOO')
    return render(request, "home.html")
