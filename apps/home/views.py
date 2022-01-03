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
from django.views import View
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
        print(request.POST)
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
    game = Game.objects.get(id=pk)
    homeTeam = Team.objects.get(id=game.homeTeam_id)
    awayTeam = Team.objects.get(id=game.awayTeam_id)
    currentSeason = Season.objects.get(currentSeason=True)

    if request.method == 'POST':
        if 'submitRoster' in request.POST:
            print('submitRoster Was Pressed')

            # homePlayedList = request.POST.getlist('homePlayed')
            # awayPlayedList = request.POST.getlist('awayPlayed')

            formsetHome = PlayerFormSet(data=request.POST, prefix='home')
            formsetAway = PlayerFormSet(request.POST, prefix='away')

            homePlayedList = processPlayedList(request.POST.getlist('homePlayed'), formsetHome, homeTeam, currentSeason)
            awayPlayedList = processPlayedList(request.POST.getlist('awayPlayed'), formsetAway, awayTeam, currentSeason)

            homePlayersPlayed = Player.objects.filter(id__in=homePlayedList)
            awayPlayersPlayed = Player.objects.filter(id__in=awayPlayedList)

            tempGameResult = TempGameResults(game=game)
            tempGameResult.save()

            tempGameResult.homePlayers.set(homePlayersPlayed)
            tempGameResult.awayPlayers.set(awayPlayersPlayed)

            return gameReportStats(request, game)

    homeTeamPlayers = Player.objects.filter(team__id=homeTeam.id).all().values().order_by('lastName')
    awayTeamPlayers = Player.objects.filter(team__id=awayTeam.id).all().values().order_by('lastName')
    formsetHomeTeam = PlayerFormSet(queryset=Player.objects.none(), prefix='home')
    formsetAwayTeam = PlayerFormSet(queryset=Player.objects.none(), prefix='away')

    context = {
        'homeTeam': homeTeam,
        'awayTeam': awayTeam,
        'homeTeamPlayers': homeTeamPlayers,
        'awayTeamPlayers': awayTeamPlayers,
        'formsetHomeTeam': formsetHomeTeam,
        'formsetAwayTeam': formsetAwayTeam,
    }

    return render(request, "home/game-report-roster.html", context)


@login_required(login_url="/login/")
def gameReportStats(request, game):
    tempGameResult = TempGameResults.objects.get(game=game)
    # teams = Team.objects.filter(id__in=teamList)
    homeTeam = Team.objects.get(id=game.homeTeam_id)
    awayTeam = Team.objects.get(id=game.awayTeam_id)
    teamList = [homeTeam.id, awayTeam.id]
    teams = Team.objects.filter(id__in=teamList)
    homePlayersPlayed = Player.objects.filter(id__in=tempGameResult.homePlayers.values_list('id'))
    awayPlayersPlayed = Player.objects.filter(id__in=tempGameResult.awayPlayers.values_list('id'))

    gameResultForm = GameResultForm(teams=teams)

    formsetGoalHome = GoalFormSet(
        queryset=Goal.objects.none(),
        form_kwargs={'players': homePlayersPlayed},
        prefix='goalHome'
    )
    formsetGoalAway = GoalFormSet(
        queryset=Goal.objects.none(),
        form_kwargs={'players': awayPlayersPlayed},
        prefix='goalAway'
    )
    formsetPenaltyHome = PenaltyFormSet(
        queryset=Penalty.objects.none(),
        form_kwargs={'players': homePlayersPlayed},
        prefix='penaltyHome'
    )
    formsetPenaltyAway = PenaltyFormSet(
        queryset=Penalty.objects.none(),
        form_kwargs={'players': awayPlayersPlayed},
        prefix='penaltyAway'
    )

    context = {
        'formsetGoalHome': formsetGoalHome,
        'formsetPenaltyHome': formsetPenaltyHome,
        'formsetGoalAway': formsetGoalAway,
        'formsetPenaltyAway': formsetPenaltyAway,
        'gameResultForm': gameResultForm,
        'homeTeam': homeTeam,
        'awayTeam': awayTeam,
    }

    if request.method == 'POST':
        print('Test')
    #     if 'submitAll' in request.POST:
    #         formsetPenalty2 = PenaltyFormSet(data=request.POST, prefix='penalty')
    #         formsetGoal2 = GoalFormSet(data=request.POST, prefix='goal')
    #         print(formsetPenalty2)
    #         print(formsetGoal2)
    return render(request, "home/game-report-stats.html", context)


# @login_required(login_url="/login/")
# class GameReportStats(View):
#     template_name = 'home/game-report-stats.html'
#     gameResultForm = None
#     formsetGoal = None
#     formsetPenalty = None
#
#     def get(self, request, *args, **kwargs):

def processPlayedList(postList, formset, team, currentSeason):
    playedList = postList

    for player in postList:
        playedPlayer = Player.objects.get(id=player)
        playerStatObj = PlayerStats.objects.get(player=playedPlayer)
        playerStatObj.gamesPlayed = playerStatObj.gamesPlayed + 1
        playerStatObj.save()

    if formset.is_valid():
        for form in formset:
            newPlayer = form.save(commit=False)
            newPlayer.team = team
            newPlayer.save()
            playedList.append(newPlayer.id)
            try:
                playerStatObj = PlayerStats.objects.get(player=newPlayer)
            except:
                print('Player Stats Does not Exist')
            else:
                playerStatObj.season = currentSeason
                playerStatObj.gamesPlayed = playerStatObj.gamesPlayed + 1
                playerStatObj.save()

    return playedList
