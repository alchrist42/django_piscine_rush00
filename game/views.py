from django.shortcuts import render

def index(request):
    return render(None, 'game/index.html')
