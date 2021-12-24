# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from .models import *
from .forms import *


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def divisions(request):
    divisions = Division.objects.all().values()
    context = {'divisions': divisions}
    return render(request, "home/divisions.html", context)


@login_required(login_url="/login/")
def referees(request):
    referees = Referee.objects.all().values()
    context = {'referees': referees}
    return render(request, "home/referees.html", context)


@login_required(login_url="/login/")
def rinks(request):
    rinks = Rink.objects.all().values()
    context = {'rinks': rinks}
    return render(request, "home/rinks.html", context)


@login_required(login_url="/login/")
def scorekeepers(request):
    scorekeepers = Scorekeeper.objects.all().values()
    context = {'scorekeepers': scorekeepers}
    return render(request, "home/scorekeepers.html", context)


@login_required(login_url="/login/")
def divisionsAndTeams(request):
    divisions = Division.objects.all().values()
    teams = Team.objects.all().values()
    context = {'divisions': divisions, 'teams': teams}
    return render(request, "home/divisions-teams.html", context)


@login_required(login_url="/login/")
def addSeason(request):
    form = SeasonForm()
    if request.method == 'POST':
        form = SeasonForm(request.POST)
        if form.is_valid():
            seasonName = form.cleaned_data['name']
            print(seasonName)
            form.save()
            if 'seasonImport' in request.POST:
                season = Season.objects.get(name=seasonName)
                seasonImport(season)
                # If season import is checked
                return redirect('gameManager')
            return redirect('home')
    context = {'form': form}
    return render(request, "home/create-new-season.html", context)


@login_required(login_url="/login/")
def iceSlotManager(request):
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        formset = IceSlotFormSet(queryset=IceSlot.objects.none())
    elif request.method == 'POST':
        formset = IceSlotFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save()
            return redirect('home')
    context = {'formset': formset}
    return render(request, "home/ice-slot-manager.html", context)


@login_required(login_url="/login/")
def gameManager(request):
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        formset = GameFormSet(queryset=Game.objects.none())
    elif request.method == 'POST':
        formset = GameFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save()
            return redirect('home')
    context = {'formset': formset}
    return render(request, "home/game-manager.html", context)


@login_required(login_url="/login/")
def selectGame(request):
    games = Game.objects.all().values(
        'iceSlot__date',
        'homeTeam__name',
        'awayTeam__name',
        'id'
    )
    context = {'games': games}
    return render(request, "home/select-game.html", context)


@login_required(login_url="/login/")
def gameReportRoster(request, pk):
    # Need to add in to the Game Form, the season for the game
    game = Game.objects.get(id=pk)
    homeTeam = Team.objects.get(id=game.homeTeam_id)
    awayTeam = Team.objects.get(id=game.awayTeam_id)
    homeTeamPlayers = Player.objects.filter(team__id=homeTeam.id).all().values()
    awayTeamPlayers = Player.objects.filter(team__id=awayTeam.id).all().values()
    print(homeTeam)
    print(awayTeam)
    print('Home Team Players')
    for player in homeTeamPlayers:
        print(player['firstName'] + " " + player['lastName'])
    print('Away Team Players')
    for player2 in awayTeamPlayers:
        print(player2['firstName'] + " " + player2['lastName'])

    games = Game.objects.all().values(
        'iceSlot__date',
        'homeTeam__name',
        'awayTeam__name',
        'id'
    )
    context = {'games': games,
               'homeTeam': homeTeam,
               'awayTeam': awayTeam,
               'homeTeamPlayers': homeTeamPlayers,
               'awayTeamPlayers': awayTeamPlayers
               }
    return render(request, "home/game-report-roster.html", context)
