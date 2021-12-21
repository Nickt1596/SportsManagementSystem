# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('referees/', views.referees, name="referees"),
    path('rinks/', views.rinks, name="rinks"),
    path('game-form/', views.addGame, name="addGame"),
    path('ice-slot-manager/', views.iceSlotManager, name="iceSlotManager"),
    path('game-manager/', views.gameManager, name="gameManager"),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),


]
