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
from django.db.models import Count, OuterRef, Exists, Q
from django.views import View
from .models import *
from .forms import *


@login_required(login_url="/login/")
def index(request):
    context = {"segment": "index"}

    html_template = loader.get_template("home/index.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split("/")[-1]

        if load_template == "admin":
            return HttpResponseRedirect(reverse("admin:index"))
        context["segment"] = load_template

        html_template = loader.get_template("home/" + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template("home/page-404.html")
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template("home/page-500.html")
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def adminHome(request):
    gamesNeedRefs = (
        Game.objects.annotate(referee_count=Count("referees"))
            .filter(referee_count__lt=2)
            .values(
            "iceSlot__date",
            "iceSlot__rink__name",
            "iceSlot__time",
            "homeTeam__name",
            "awayTeam__name",
        )
    )
    gamesNeedScorekeepers = (
        Game.objects.annotate(scorekeeper_count=Count("scorekeeper"))
            .filter(scorekeeper_count__lt=1)
            .values(
            "iceSlot__date",
            "iceSlot__rink__name",
            "iceSlot__time",
            "homeTeam__name",
            "awayTeam__name",
        )
    )

    gameNeedResults = Game.objects.filter(
        ~Exists(GameResult.objects.filter(game=OuterRef("id")))
    ).values("iceSlot__date", "homeTeam__name", "awayTeam__name", "scorekeeper__name")

    todaysGames = Game.objects.filter(iceSlot__date=date.today()).values(
        "iceSlot__date", "iceSlot__time", "homeTeam__name", "awayTeam__name"
    )

    divisionStandings = Division.objects.all().values(
        "name",
        "id",
        "team__name",
        "team__id",
        "team__teamstats__regWins",
        "team__teamstats__regLoses",
        "team__teamstats__ties",
        "team__teamstats__otLoses",
        "team__teamstats__otWins",
        "team__teamstats__points",
    )

    context = {
        "gamesNeedRefs": gamesNeedRefs,
        "gamesNeedScorekeepers": gamesNeedScorekeepers,
        "gameNeedResults": gameNeedResults,
        "todaysGames": todaysGames,
        "divisionStandings": divisionStandings,
    }
    return render(request, "home/admin-home.html", context)


@login_required(login_url="/login/")
def teamPage(request, pk):
    teamStats = TeamStats.objects.filter(team_id=pk).values(
        "team__name", "regWins", "regLoses", "ties", "otWins", "otLoses", "points"
    )
    playerStats = (
        PlayerStats.objects.filter(player__team__id=pk)
            .values(
            "player__firstName",
            "player__lastName",
            "player__jerseyNumber",
            "player__position",
            "gamesPlayed",
            "goals",
            "assists",
            "points",
            "penaltyMins",
        )
            .order_by("points")
    )

    teamSchedule = (
        Game.objects.filter(Q(homeTeam__id=pk) | Q(awayTeam__id=pk))
            .values(
            "homeTeam__name",
            "awayTeam__name",
            "iceSlot__date",
            "iceSlot__time",
            "iceSlot__rink__name",
            "gameresult__winningTeam__name",
            "gameresult__losingTeam__name",
            "gameresult__winnerScore",
            "gameresult__loserScore",
            "gameresult__winType",
        )
            .order_by("iceSlot__date")
    )

    context = {
        "teamStats": teamStats,
        "playerStats": playerStats,
        "teamSchedule": teamSchedule,
    }
    return render(request, "home/team-page.html", context)


@login_required(login_url="/login/")
def standings(request):
    divisionStandings = Division.objects.all().values(
        "name",
        "id",
        "team__name",
        "team__id",
        "team__teamstats__regWins",
        "team__teamstats__regLoses",
        "team__teamstats__ties",
        "team__teamstats__otLoses",
        "team__teamstats__otWins",
        "team__teamstats__points",
    )
    context = {"divisionStandings": divisionStandings}
    return render(request, "home/standings.html", context)


@login_required(login_url="/login/")
def rinks(request):
    rinks = Rink.objects.all().values()
    context = {"rinks": rinks}
    return render(request, "home/rinks.html", context)


@login_required(login_url="/login/")
def schedule(request):
    schedule = (
        Game.objects.all()
            .values(
            "homeTeam__name",
            "awayTeam__name",
            "iceSlot__date",
            "iceSlot__time",
            "iceSlot__rink__name",
            "iceSlot__id",
            "gameresult__winningTeam__name",
            "gameresult__losingTeam__name",
            "gameresult__winnerScore",
            "gameresult__loserScore",
            "gameresult__winType",
        )
            .order_by("iceSlot__date")
    )
    context = {"schedule": schedule}
    return render(request, "home/schedule.html", context)


@login_required(login_url="/login/")
def iceSlotManager(request):
    if request.method == "GET":
        # we don't want to display the already saved model instances
        formset = IceSlotFormSet(queryset=IceSlot.objects.none())
    elif request.method == "POST":
        formset = IceSlotFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save()
            return redirect("home")
    context = {"formset": formset}
    return render(request, "home/ice-slot-manager.html", context)


@login_required(login_url="/login/")
def gameManager(request):
    if request.method == "GET":
        # we don't want to display the already saved model instances
        formset = GameFormSet(queryset=Game.objects.none())
    elif request.method == "POST":
        formset = GameFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                form.save()
            return redirect("home")
    context = {"formset": formset}
    return render(request, "home/game-manager.html", context)


@login_required(login_url="/login/")
def editGames(request):
    games = (
        Game.objects.all()
            .values(
            "homeTeam__name",
            "awayTeam__name",
            "iceSlot__date",
            "iceSlot__time",
            "iceSlot__rink__name",
            "iceSlot__id",
            "gameresult__winningTeam__name",
            "gameresult__losingTeam__name",
            "gameresult__winnerScore",
            "gameresult__loserScore",
            "gameresult__winType",
        )
            .order_by("iceSlot__date")
    )
    context = {"games": games}
    return render(request, "home/edit-games.html", context)


@login_required(login_url="/login/")
def gameReportSelectGame(request):
    games = Game.objects.all().values(
        "iceSlot__date", "homeTeam__name", "awayTeam__name", "id"
    )
    context = {"games": games}
    return render(request, "home/game-report-select-game.html", context)


@login_required(login_url="/login/")
def gameReportQuick(request, pk):
    gameTeams = Game.objects.get(id=pk)
    quickGameResultForm = GameResultQuickForm(
        teams=Team.objects.filter(
            id__in=[gameTeams.homeTeam.id, gameTeams.awayTeam.id]
        )
    )
    context = {"quickGameResultForm": quickGameResultForm}
    return render(request, "home/game-report-quick.html", context)


@login_required(login_url="/login/")
def gameReportRoster(request, pk):
    game = Game.objects.get(id=pk)
    homeTeamPlayers = game.homeTeam.player_set.values()
    awayTeamPlayers = game.awayTeam.player_set.values()
    formsetHomeTeam = GameResultRosterFormSet(queryset=Player.objects.none(), prefix="home")
    formsetAwayTeam = GameResultRosterFormSet(queryset=Player.objects.none(), prefix="away")

    if request.method == "POST":
        if "submitRoster" in request.POST:
            # Holds a list of The players where the box was checked indicating that they played
            homePlayedList = request.POST.getlist('homePlayed')
            awayPlayedList = request.POST.getlist('awayPlayed')

            formsetHome = GameResultRosterFormSet(data=request.POST, prefix="home")
            formsetAway = GameResultRosterFormSet(data=request.POST, prefix="away")

            # Used to hold the IDs of newly added players, will be used if we need to delete a newly added player
            newHomePlayerList = []
            newAwayPlayerList = []

            if formsetHome.is_valid():
                for form in formsetHome:
                    newPlayer = form.save(commit=False)
                    newPlayer.team = game.homeTeam
                    newPlayer.save()
                    newHomePlayerList.append(str(newPlayer.id))

            if formsetAway.is_valid():
                for form in formsetAway:
                    newPlayer = form.save(commit=False)
                    newPlayer.team = game.awayTeam
                    newPlayer.save()
                    newAwayPlayerList.append(str(newPlayer.id))

            request.session["homePlayersPlayed"] = homePlayedList
            request.session["awayPlayersPlayed"] = awayPlayedList
            request.session["newHomePlayerList"] = newHomePlayerList
            request.session["newAwayPlayerList"] = newAwayPlayerList

            return redirect("gameReportStats", pk)

    context = {
        "game": game,
        "homeTeamPlayers": homeTeamPlayers,
        "awayTeamPlayers": awayTeamPlayers,
        "formsetHomeTeam": formsetHomeTeam,
        "formsetAwayTeam": formsetAwayTeam,
    }

    return render(request, "home/game-report-roster.html", context)


@login_required(login_url="/login/")
def gameReportStats(request, pk):
    game = Game.objects.get(id=pk)
    homePlayedList = request.session["homePlayersPlayed"]
    awayPlayedList = request.session["awayPlayersPlayed"]
    newHomePlayerList = request.session["newHomePlayerList"]
    newAwayPlayerList = request.session["newAwayPlayerList"]

    homePlayersPlayed = Player.objects.filter(Q(id__in=homePlayedList) | Q(id__in=newHomePlayerList))
    awayPlayersPlayed = Player.objects.filter(Q(id__in=awayPlayedList) | Q(id__in=newAwayPlayerList))

    gameResultForm = GameResultQuickForm(teams=Team.objects.filter(Q(id=game.homeTeam.id) | Q(id=game.awayTeam.id)))

    formsetGoalHome = GoalFormSet(
        queryset=Goal.objects.none(),
        form_kwargs={"players": homePlayersPlayed},
        prefix="goalHome",
    )
    formsetGoalAway = GoalFormSet(
        queryset=Goal.objects.none(),
        form_kwargs={"players": awayPlayersPlayed},
        prefix="goalAway",
    )
    formsetPenaltyHome = PenaltyFormSet(
        queryset=Penalty.objects.none(),
        form_kwargs={"players": homePlayersPlayed},
        prefix="penaltyHome",
    )
    formsetPenaltyAway = PenaltyFormSet(
        queryset=Penalty.objects.none(),
        form_kwargs={"players": awayPlayersPlayed},
        prefix="penaltyAway",
    )

    context = {
        "formsetGoalHome": formsetGoalHome,
        "formsetPenaltyHome": formsetPenaltyHome,
        "formsetGoalAway": formsetGoalAway,
        "formsetPenaltyAway": formsetPenaltyAway,
        "gameResultForm": gameResultForm,
        "game": game
    }

    if request.method == "POST":
        formsetGoalHome = GoalFormSet(data=request.POST, form_kwargs={"players": homePlayersPlayed}, prefix="goalHome")
        formsetGoalAway = GoalFormSet(data=request.POST, form_kwargs={"players": awayPlayersPlayed}, prefix="goalAway")
        formsetPenaltyHome = PenaltyFormSet(data=request.POST, form_kwargs={"players": homePlayersPlayed},
                                            prefix="penaltyHome")
        formsetPenaltyAway = PenaltyFormSet(data=request.POST, form_kwargs={"players": awayPlayersPlayed},
                                            prefix="penaltyAway")
        gameResultForm = GameResultQuickForm(request.POST,
                                             teams=Team.objects.filter(Q(id=game.homeTeam.id) | Q(id=game.awayTeam.id)))

        if formsetGoalHome.is_valid():
            for form in formsetGoalHome:
                newGoal = form.save(commit=False)
                print(newGoal)
        if formsetGoalAway.is_valid():
            for form in formsetGoalAway:
                newGoal = form.save(commit=False)
                print(newGoal)
        if formsetPenaltyHome.is_valid():
            for form in formsetPenaltyHome:
                newPenalty = form.save(commit=False)
                print(newPenalty)
        if formsetPenaltyAway.is_valid():
            for form in formsetPenaltyAway:
                newPenalty = form.save(commit=False)
                print(newPenalty)

        if gameResultForm.is_valid():
            print(gameResultForm.cleaned_data)

        return redirect("home")

    return render(request, "home/game-report-stats.html", context)


# ALL OLD VIEWS BELOW
# ALL OLD VIEWS BELOW
# ALL OLD VIEWS BELOW
# ALL OLD VIEWS BELOW
# ALL OLD VIEWS BELOW
# ALL OLD VIEWS BELOW


@login_required(login_url="/login/")
def addSeason(request):
    form = SeasonForm()
    if request.method == "POST":
        form = SeasonForm(request.POST)
        if form.is_valid():
            seasonName = form.cleaned_data["name"]
            print(seasonName)
            form.save()
            if "seasonImport" in request.POST:
                season = Season.objects.get(name=seasonName)
                seasonImport(season)
                # If season import is checked
                return redirect("gameManager")
            return redirect("home")
    context = {"form": form}
    return render(request, "home/create-new-season.html", context)


@login_required(login_url="/login/")
def addDivision(request):
    # form = DivisionForm()
    form = PlayerForm()
    if request.method == "POST":
        # form = DivisionForm(request.POST)
        form = PlayerForm(request.POST)
        print(form)
        if form.is_valid():
            print("Is valid")
            # divisionName = form.cleaned_data["divisionName"]
            # print(divisionName)
            # form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "home/add-division.html", context)


# We will need to modify this to make it so it doesn't actually update games played until we confirm the results
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
                print("Player Stats Does not Exist")
            else:
                playerStatObj.season = currentSeason
                playerStatObj.gamesPlayed = playerStatObj.gamesPlayed + 1
                playerStatObj.save()

    return playedList


def processGoals(formset, game):
    if formset.is_valid():
        for form in formset:
            goal = form.save(commit=False)
            goal.game = game
            goal.save()
            updatePlayerStatsGoal(goal.goalScorer)
            if goal.assistPrimary is not None:
                updatePlayerStatsAssist(goal.assistPrimary)
            if goal.assistSecondary is not None:
                updatePlayerStatsAssist(goal.assistSecondary)


def processPenalties(formset, game):
    print("Hold")


def updatePlayerStatsGoal(goalScorer):
    playerStats = PlayerStats.objects.get(id=goalScorer.id)
    playerStats.goals = playerStats.goals + 1
    playerStats.save()


def updatePlayerStatsAssist(goalAssist):
    playerStats = PlayerStats.objects.get(id=goalAssist.id)
    playerStats.goals = playerStats.assists + 1
    playerStats.save()
