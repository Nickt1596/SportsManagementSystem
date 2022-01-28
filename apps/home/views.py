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
    if request.user.type == 'COMMISSIONER':
        return redirect(adminHome)
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
def scorekeepers(request):
    scorekeepers = Scorekeeper.objects.all().values()
    context = {"scorekeepers": scorekeepers}
    return render(request, "home/scorekeepers.html", context)

@login_required(login_url="/login/")
def referees(request):
    referees = Referee.objects.all().values()
    context = {"referees": referees}
    return render(request, "home/referees.html", context)


@login_required(login_url="/login/")
def schedule(request):
    schedule = (
        Game.objects.all()
            .values(
            "homeTeam__name",
            "homeTeam__id",
            "awayTeam__name",
            "awayTeam__id",
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


"""
Stage 1 of the Game Report Function - Game Selection
User has the option to enter a Quick Report or Full Report
"""


@login_required(login_url="/login/")
def gameReportSelectGame(request):
    games = Game.objects.all().values(
        "iceSlot__date", "homeTeam__name", "awayTeam__name", "id"
    )
    context = {"games": games}
    return render(request, "home/game-report-select-game.html", context)


"""
Stage 1a. of the Game Report Function - Quick Report
User Selects Winning and Losing Team, Winner and Loser Score, and the win Type. 
User will need to return later to complete the rest of the steps of the Game Report
"""


@login_required(login_url="/login/")
def gameReportQuick(request, pk):
    gameTeams = Game.objects.get(id=pk)
    quickGameResultForm = GameResultQuickForm(
        teams=Team.objects.filter(id__in=[gameTeams.homeTeam.id, gameTeams.awayTeam.id])
    )
    context = {"quickGameResultForm": quickGameResultForm}
    return render(request, "home/game-report-quick.html", context)


"""
Stage 2. of the Game Report Function - Full Report - Enter Roster
Creates a Table w/ Checkbox selection for the roster of the Home and Away Team. 
Checking the box indicates the player has played in the game. 
Create a Formset to add a New player for the Home and Away Team

When submitted the following happens 
1. We create a list of for the Home Players and Away Players that had their checkbox selected. 
2. We generate the formset for the Home and Away Team, validate the form data and save it to the database
   as well as save the newPlayer.Id and add it to a list for the respective team. 
3. These 4 lists get saved to session variables and we redirect to the enter Stats page
"""


@login_required(login_url="/login/")
def gameReportRoster(request, pk):
    game = Game.objects.get(id=pk)
    homeTeamPlayers = game.homeTeam.player_set.values()
    awayTeamPlayers = game.awayTeam.player_set.values()
    formsetHomeTeam = GameResultRosterFormSet(
        queryset=Player.objects.none(), prefix="home"
    )
    formsetAwayTeam = GameResultRosterFormSet(
        queryset=Player.objects.none(), prefix="away"
    )

    if request.method == "POST":
        if "submitRoster" in request.POST:
            # Holds a list of The players where the box was checked indicating that they played
            homePlayedList = request.POST.getlist("homePlayed")
            awayPlayedList = request.POST.getlist("awayPlayed")

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


"""
Stage 3. of the Game Report Function - Full Report - Enter Stats
We get our session variables we stored from Roster 
We then do the following 
1. Query for the HomePlayersPlayed and AwayPlayersPlay
2. A gameResult Form 
3. Formset for Goals and Penalties for the respective teams
"""


@login_required(login_url="/login/")
def gameReportStats(request, pk):
    game = Game.objects.get(id=pk)
    homePlayedList = request.session["homePlayersPlayed"]
    awayPlayedList = request.session["awayPlayersPlayed"]
    newHomePlayerList = request.session["newHomePlayerList"]
    newAwayPlayerList = request.session["newAwayPlayerList"]

    homePlayersPlayed = Player.objects.filter(
        Q(id__in=homePlayedList) | Q(id__in=newHomePlayerList)
    )
    awayPlayersPlayed = Player.objects.filter(
        Q(id__in=awayPlayedList) | Q(id__in=newAwayPlayerList)
    )

    gameResultForm = GameResultQuickForm(
        teams=Team.objects.filter(Q(id=game.homeTeam.id) | Q(id=game.awayTeam.id))
    )

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
        "game": game,
    }

    if request.method == "POST":
        homeGoals = []
        homePenalties = []
        awayGoals = []
        awayPenalties = []
        formsetGoalHome = GoalFormSet(
            data=request.POST,
            form_kwargs={"players": homePlayersPlayed},
            prefix="goalHome",
        )
        formsetGoalAway = GoalFormSet(
            data=request.POST,
            form_kwargs={"players": awayPlayersPlayed},
            prefix="goalAway",
        )
        formsetPenaltyHome = PenaltyFormSet(
            data=request.POST,
            form_kwargs={"players": homePlayersPlayed},
            prefix="penaltyHome",
        )
        formsetPenaltyAway = PenaltyFormSet(
            data=request.POST,
            form_kwargs={"players": awayPlayersPlayed},
            prefix="penaltyAway",
        )
        gameResultForm = GameResultQuickForm(
            request.POST,
            teams=Team.objects.filter(Q(id=game.homeTeam.id) | Q(id=game.awayTeam.id)),
        )

        if formsetGoalHome.is_valid():
            for form in formsetGoalHome:
                newGoal = form.save()
                homeGoals.append(str(newGoal.id))
        if formsetGoalAway.is_valid():
            for form in formsetGoalAway:
                newGoal = form.save()
                awayGoals.append(str(newGoal.id))
        if formsetPenaltyHome.is_valid():
            for form in formsetPenaltyHome:
                newPenalty = form.save()
                homePenalties.append(str(newPenalty.id))
        if formsetPenaltyAway.is_valid():
            for form in formsetPenaltyAway:
                newPenalty = form.save()
                awayPenalties.append(str(newPenalty.id))

        if gameResultForm.is_valid():
            gameResult = gameResultForm.save(commit=False)
            gameResult.game = game
            gameResult.save()

        # Function used to update Games Played for the Player Stats
        playerList = homePlayedList + awayPlayedList + newHomePlayerList + newAwayPlayerList
        addGamePlayed(playerList)
        return redirect("home")

    return render(request, "home/game-report-stats.html", context)


@login_required(login_url="/login/")
def addRink(request):
    form = RinkForm()
    title = "Add Rink"
    if request.method == 'POST':
        form = RinkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rinks')
    context = {'form': form, 'title': title}
    return render(request, "home/generic-form.html", context)


@login_required(login_url="/login/")
def updateRink(request, pk):
    rink = Rink.objects.get(id=pk)
    form = RinkForm(instance=rink)
    title = "Update " + str(rink.name)
    if request.method == 'POST':
        form = RinkForm(request.POST, instance=rink)
        if form.is_valid():
            form.save()
            return redirect('rinks')
    context = {'form': form, 'title': title}
    return render(request, "home/generic-form.html", context)


@login_required(login_url="/login/")
def addScorekeeper(request):
    form = ScorekeeperForm()
    title = "Add Scorekeeper"
    if request.method == 'POST':
        form = ScorekeeperForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('scorekeepers')
    context = {'form': form, 'title': title}
    return render(request, "home/generic-form.html", context)


@login_required(login_url="/login/")
def updateScorekeeper(request, pk):
    scorekeeper = Scorekeeper.objects.get(id=pk)
    form = ScorekeeperForm(instance=scorekeeper)
    title = "Update " + str(scorekeeper.name)
    if request.method == 'POST':
        form = ScorekeeperForm(request.POST, instance=scorekeeper)
        if form.is_valid():
            form.save()
            return redirect('scorekeepers')
    context = {'form': form, 'title': title}
    return render(request, "home/generic-form.html", context)


@login_required(login_url="/login/")
def addReferee(request):
    form = RefereeForm()
    title = "Add Referee"
    if request.method == 'POST':
        form = RefereeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('referees')
    context = {'form': form, 'title': title}
    return render(request, "home/generic-form.html", context)


@login_required(login_url="/login/")
def updateReferee(request, pk):
    referee = Referee.objects.get(id=pk)
    form = RefereeForm(instance=referee)
    title = "Update " + str(referee.name)
    if request.method == 'POST':
        form = RefereeForm(request.POST, instance=referee)
        if form.is_valid():
            form.save()
            return redirect('referees')
    context = {'form': form, 'title': title}
    return render(request, "home/generic-form.html", context)


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


# Utility Function used to increment games Played by 1
def addGamePlayed(playerList):
    playerStats = PlayerStats.objects.filter(player__id__in=playerList)
    for player in playerStats:
        player.gamesPlayed = player.gamesPlayed + 1
        player.save()
