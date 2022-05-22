from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def index(request):
    return render(None, 'game/index.html')

def move(request, direction):
    return HttpResponse("move to the " + direction)

def start(request):
    return HttpResponse("pressed start")

def select(request):
    return HttpResponse("pressed select")

def btn_a(request):
    return HttpResponse("pressed A")

def btn_b(request):
    return HttpResponse("pressed B")

def worldmap(request):
    gmap = [["#"] * 10 for _ in range(10)]
    gmap[5][5] = "@"
    gmap[3][5] = "?"

    return render(None, 'game/worldmap.html', {"worldmap": gmap})
