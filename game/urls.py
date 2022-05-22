from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('move/<str:direction>', views.move, name='move'),
    path('start', views.start, name='start'),
    path('select', views.select, name='select'),
    path('btn_a', views.btn_a, name='btn_a'),
    path('btn_b', views.btn_b, name='btn_b'),
    path('worldmap', views.worldmap, name='worldmap'),
    path('battle', views.battle, name='battle'),
   
]
    