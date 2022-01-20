# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from apps.home import views

urlpatterns = [

    # The home page
    # Good URLS Below
    path('', views.index, name='home'),
    path('admin-home/', views.adminHome, name="adminHome"),
    path('team-page/<str:pk>', views.teamPage, name="teamPage"),
    path('standings/', views.standings, name="standings"),
    path('schedule/', views.schedule, name="schedule"),
    path('ice-slot-manager/', views.iceSlotManager, name="iceSlotManager"),
    path('game-manager/', views.gameManager, name="gameManager"),
    path('edit-games/', views.editGames, name="editGames"),
    path('game-report-select-game/', views.gameReportSelectGame, name="gameReportSelectGame"),
    path('game-report-quick/<str:pk>', views.gameReportQuick, name="gameReportQuick"),
    path('game-report-stats/<str:pk>', views.gameReportStats, name="gameReportStats"),


    # URLS still needing updating below
    path('add-division/', views.addDivision, name="addDivision"),
    path('rinks/', views.rinks, name="rinks"),
    path('create-new-season/', views.addSeason, name="addSeason"),
    path('game-report-roster/<str:pk>', views.gameReportRoster, name="gameReportRoster"),
    path('game-report-stats/<str:gameId>', views.gameReportStats, name="gameReportStats"),
    path('__debug__/', include('debug_toolbar.urls')),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),


]
