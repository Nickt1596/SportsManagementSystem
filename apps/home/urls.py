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

    path('rinks/', views.rinks, name="rinks"),
    path('add-rink/', views.addRink, name="addRink"),
    path('update-rink/<str:pk>', views.updateRink, name="updateRink"),

    path('scorekeepers/', views.scorekeepers, name="scorekeepers"),
    path('add-scorekeeper/', views.addScorekeeper, name="addScorekeeper"),
    path('update-updatescorekeeper/<str:pk>', views.updateScorekeeper, name="updateScorekeeper"),

    path('referees/', views.referees, name="referees"),
    path('add-referee/', views.addReferee, name="addReferee"),
    path('update-updatereferee/<str:pk>', views.updateReferee, name="updateReferee"),


    # URLS still needing updating below
    path('add-division/', views.addDivision, name="addDivision"),
    path('create-new-season/', views.addSeason, name="addSeason"),
    path('game-report-roster/<str:pk>', views.gameReportRoster, name="gameReportRoster"),
    path('game-report-stats/<str:gameId>', views.gameReportStats, name="gameReportStats"),
    path('__debug__/', include('debug_toolbar.urls')),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),


]
