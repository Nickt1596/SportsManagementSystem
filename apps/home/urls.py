# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('admin-home/', views.adminHome, name="adminHome"),
    path('add-division/', views.addDivision, name="addDivision"),
    path('referees/', views.referees, name="referees"),
    path('scorekeepers/', views.scorekeepers, name="scorekeepers"),
    path('rinks/', views.rinks, name="rinks"),
    path('divisions/', views.divisions, name="divisions"),
    path('divisions-teams/', views.divisionsAndTeams, name="divisionsAndTeams"),
    path('ice-slot-manager/', views.iceSlotManager, name="iceSlotManager"),
    path('game-manager/', views.gameManager, name="gameManager"),
    path('create-new-season/', views.addSeason, name="addSeason"),
    path('select-game/', views.selectGame, name="selectGame"),
    path('game-report-roster/<str:pk>', views.gameReportRoster, name="gameReportRoster"),
    path('game-report-stats/<str:gameId>', views.gameReportStats, name="gameReportStats"),
    path('__debug__/', include('debug_toolbar.urls')),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),


]
