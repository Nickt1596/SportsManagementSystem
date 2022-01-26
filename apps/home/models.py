# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
import uuid
from decimal import *
from datetime import *
import names
import random


class Season(models.Model):
    name = models.CharField(max_length=50)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    numGames = models.CharField(max_length=3)
    seasonCompleted = models.BooleanField(default=False)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name


class Division(models.Model):
    # One Season, Many divisions
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.season.name + " " + self.name


class Team(models.Model):
    # One Division, Many Teams
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding is True:
            super().save(*args, **kwargs)
            teamStats = TeamStats(team_id=self.id)
            teamStats.save()


class Player(models.Model):
    # One Team, Many Players
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=80)
    lastName = models.CharField(max_length=80)
    jerseyNumber = models.CharField(max_length=3)
    position = models.CharField(max_length=80, blank=True, null=True)
    captain = models.BooleanField(default=False)
    altCaptain = models.BooleanField(default=False)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return "#" + self.jerseyNumber + " " + self.firstName + ". " + self.lastName

    def save(self, *args, **kwargs):
        if self._state.adding is True:
            super().save(*args, **kwargs)
            playerStats = PlayerStats(player_id=self.id)
            playerStats.save()

        # return '#' + self.jerseyNumber + ' ' + self.firstName[0] + '. ' + self.lastName


class PlayerStats(models.Model):
    # One Player, One Player Stats
    player = models.OneToOneField(Player, on_delete=models.CASCADE)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    penaltyMins = models.IntegerField(default=0)
    gamesPlayed = models.IntegerField(default=0)
    playoffEligible = models.BooleanField(default=False)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return (
                "#"
                + self.player.jerseyNumber
                + " "
                + self.player.firstName
                + ". "
                + self.player.lastName
        )


class TeamStats(models.Model):
    # One Team, One Team Stats
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    regWins = models.IntegerField(default=0)
    regLoses = models.IntegerField(default=0)
    otWins = models.IntegerField(default=0)
    otLoses = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    goalsFor = models.IntegerField(default=0)
    goalsAgainst = models.IntegerField(default=0)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.team.name


class Scorekeeper(models.Model):
    name = models.CharField(max_length=80)
    phoneNumber = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name


class Referee(models.Model):
    name = models.CharField(max_length=80)
    phoneNumber = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name


class Rink(models.Model):
    name = models.CharField(max_length=80)
    streetAddress = models.CharField(max_length=150)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    zip = models.CharField(max_length=80)
    phoneNumber = models.CharField(max_length=80)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.name


class IceSlot(models.Model):
    # One Rink, Many Ice Slots
    rink = models.ForeignKey(Rink, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    available = models.BooleanField(default=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.rink.name + " " + str(self.date) + " " + str(self.time)


class Game(models.Model):
    GAME_TYPE = [
        ("Exhibition", "Exhibition"),
        ("Regular Season", "Regular Season"),
        ("Playoff", "Playoff"),
        ("Championship", "Championship"),
    ]
    # One Home Team, Many Games
    homeTeam = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="Home_Team"
    )
    # One Away Team, Many Games
    awayTeam = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="Away_Team"
    )
    # One Ice Slot, One Game
    iceSlot = models.OneToOneField(
        IceSlot,
        on_delete=models.CASCADE,
        limit_choices_to={"available": True},
    )
    # One Scorekeeper, Many Games
    # Null/Blank = True in case scorekeeper not scheduled at time of creating the game
    scorekeeper = models.ForeignKey(
        Scorekeeper, on_delete=models.CASCADE, null=True, blank=True
    )
    # Many Refs, Many Games
    # Null/Blank = True in case referees not scheduled at time of creating the game
    referees = models.ManyToManyField(Referee, blank=True)
    gameType = models.CharField(max_length=100, choices=GAME_TYPE)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.homeTeam.name + " vs " + self.awayTeam.name

    # Overriding Save Method to mark the iceSlot selected as available or not available
    def save(self, *args, **kwargs):
        created = self._state.adding is True
        if created:
            iceslot = IceSlot.objects.get(id=self.iceSlot.id)
            iceslot.available = False
            iceslot.save()
        else:
            oldGame = Game.objects.get(id=self.id)
            oldIceSlot = IceSlot.objects.get(id=oldGame.iceSlot.id)
            oldIceSlot.available = True
            oldIceSlot.save()
            iceslot = IceSlot.objects.get(id=self.iceSlot.id)
            iceslot.available = False
            iceslot.save()
        super().save(*args, **kwargs)


class GameResult(models.Model):
    WIN_TYPES = [
        ("Regulation", "REG"),
        ("Overtime", "OT"),
        ("Shootout", "SO"),
        ("Tie", "TIE"),
    ]
    # One Game, One Game Result
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    # One Winning Team, many game results
    winningTeam = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="Winning_Team"
    )
    # One Losing Team, many game results
    losingTeam = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="Losing_Team"
    )
    winType = models.CharField(max_length=100, choices=WIN_TYPES)
    winnerScore = models.IntegerField()
    loserScore = models.IntegerField()
    # Quick Report used when only entering the score of the game
    quickReport = models.BooleanField(default=False)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.game.homeTeam.name + " vs " + self.game.awayTeam.name + " Result"

    # Update Team Stats
    def save(self, *args, **kwargs):
        created = self._state.adding is True
        if created:
            self.updatePoints(self.winningTeam.id, self.losingTeam.id)
            self.updateGoals(self.winningTeam.id, self.losingTeam.id)
        else:
            oldGameResult = GameResult.objects.get(id=self.id)
            self.removePoints(
                oldGameResult.winningTeam.id, oldGameResult.losingTeam.id, oldGameResult
            )
            self.removeGoals(
                oldGameResult.winningTeam.id, oldGameResult.losingTeam.id, oldGameResult
            )
            self.updatePoints(self.winningTeam.id, self.losingTeam.id)
            self.updateGoals(self.winningTeam.id, self.losingTeam.id)
        super().save(*args, **kwargs)

    def updatePoints(self, winningTeamId, losingTeamId):
        winningTeamStats = TeamStats.objects.get(team__id=winningTeamId)
        losingTeamStats = TeamStats.objects.get(team__id=losingTeamId)
        if self.winType == "Regulation":
            winningTeamStats.regWins += 1
            winningTeamStats.points += 3
            winningTeamStats.save()
            losingTeamStats.regLoses += 1
            losingTeamStats.save()
        elif self.winType == "Overtime" or self.winType == "Shootout":
            winningTeamStats.otWins += 1
            winningTeamStats.points += 2
            winningTeamStats.save()
            losingTeamStats.otLoses += 1
            losingTeamStats.points += 1
            losingTeamStats.save()
        else:
            winningTeamStats.ties += 1
            winningTeamStats.points += 1
            winningTeamStats.save()
            losingTeamStats.ties += 1
            losingTeamStats.points += 1
            losingTeamStats.save()

    def updateGoals(self, winningTeamId, losingTeamId):
        winningTeamStats = TeamStats.objects.get(team__id=winningTeamId)
        losingTeamStats = TeamStats.objects.get(team__id=losingTeamId)
        winningTeamStats.goalsFor = winningTeamStats.goalsFor + self.winnerScore
        winningTeamStats.goalsAgainst = winningTeamStats.goalsAgainst + self.loserScore
        winningTeamStats.save()
        losingTeamStats.goalsFor = losingTeamStats.goalsFor + self.loserScore
        losingTeamStats.goalsAgainst = losingTeamStats.goalsAgainst + self.winnerScore
        losingTeamStats.save()

    def removePoints(self, winningTeamId, losingTeamId, oldGameResult):
        winningTeamStats = TeamStats.objects.get(team__id=winningTeamId)
        losingTeamStats = TeamStats.objects.get(team__id=losingTeamId)
        if oldGameResult.winType == "Regulation":
            winningTeamStats.regWins -= 1
            winningTeamStats.points -= 3
            winningTeamStats.save()
            losingTeamStats.regLoses -= 1
            losingTeamStats.save()
        elif oldGameResult.winType == "Overtime" or oldGameResult.winType == "Shootout":
            winningTeamStats.otWins -= 1
            winningTeamStats.points -= 2
            winningTeamStats.save()
            losingTeamStats.otLoses -= 1
            losingTeamStats.points -= 1
            losingTeamStats.save()
        else:
            winningTeamStats.ties -= 1
            winningTeamStats.points -= 1
            winningTeamStats.save()
            losingTeamStats.ties -= 1
            losingTeamStats.points -= 1
            losingTeamStats.save()

    def removeGoals(self, winningTeamId, losingTeamId, oldGameResult):
        winningTeamStats = TeamStats.objects.get(team__id=winningTeamId)
        losingTeamStats = TeamStats.objects.get(team__id=losingTeamId)
        winningTeamStats.goalsFor = (
                winningTeamStats.goalsFor - oldGameResult.winnerScore
        )
        winningTeamStats.goalsAgainst = (
                winningTeamStats.goalsAgainst - oldGameResult.loserScore
        )
        winningTeamStats.save()
        losingTeamStats.goalsFor = losingTeamStats.goalsFor - oldGameResult.loserScore
        losingTeamStats.goalsAgainst = (
                losingTeamStats.goalsAgainst - oldGameResult.winnerScore
        )
        losingTeamStats.save()


class Goal(models.Model):
    PERIODS = [("1", "1"), ("2", "2"), ("3", "3"), ("OT", "OT")]

    # One Player, Many Goals
    goalScorer = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name="Goal_Scorer"
    )
    # One Player, Many Primary Assists
    assistPrimary = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="Primary_Assist",
    )
    # One Player, Many Secondary Assists
    assistSecondary = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="Secondary_Assist",
    )
    period = models.CharField(max_length=100, choices=PERIODS)
    timeScored = models.CharField(max_length=80)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    # Overriding Save Method to update the players stats when a goal is goal is added
    def save(self, *args, **kwargs):
        created = self._state.adding is True
        if created:
            self.addGoal(self.goalScorer.id)
            if self.assistPrimary is not None:
                self.addAssist(self.assistPrimary.id)
            if self.assistSecondary is not None:
                self.addAssist(self.assistSecondary.id)
        else:
            oldGoal = Goal.objects.get(id=self.id)
            if self.goalScorer.id != oldGoal.goalScorer.id:
                self.removeGoal(oldGoal.goalScorer.id)
                self.addGoal(self.goalScorer.id)
            if (
                    self.assistPrimary is not None
                    and self.assistPrimary.id != oldGoal.assistPrimary.id
            ):
                self.addAssist(self.assistPrimary.id)
                if oldGoal.assistPrimary is not None:
                    self.removeAssist(oldGoal.assistPrimary.id)
            if (
                    self.assistSecondary is not None
                    and self.assistSecondary.id != oldGoal.assistSecondary.id
            ):
                self.addAssist(self.assistSecondary.id)
                if oldGoal.assistSecondary is not None:
                    self.removeAssist(oldGoal.assistSecondary.id)
        super().save(*args, **kwargs)

    def addGoal(self, playerId):
        playerStats = PlayerStats.objects.get(player__id=playerId)
        playerStats.goals = playerStats.goals + 1
        playerStats.points = playerStats.points + 1
        playerStats.save()

    def addAssist(self, playerId):
        playerStats = PlayerStats.objects.get(player__id=playerId)
        playerStats.assists = playerStats.goals + 1
        playerStats.points = playerStats.points + 1
        playerStats.save()

    def removeGoal(self, playerId):
        playerStats = PlayerStats.objects.get(player__id=playerId)
        playerStats.goals = playerStats.goals - 1
        playerStats.points = playerStats.points - 1
        playerStats.save()

    def removeAssist(self, playerId):
        playerStats = PlayerStats.objects.get(player__id=playerId)
        playerStats.assists = playerStats.goals - 1
        playerStats.points = playerStats.points - 1
        playerStats.save()


class Penalty(models.Model):
    PERIODS = [("1", "1"), ("2", "2"), ("3", "3"), ("OT", "OT")]
    PENALTY_SEVERITY = [
        ("Minor", "Minor"),
        ("Double Minor", "Double Minor"),
        ("Major", "Major"),
        ("Game Misconduct", "Game Misconduct"),
        ("Match", "Match"),
    ]
    PENALTY_LENGTH = [("2", "2"), ("4", "4"), ("5", "5"), ("10", "10")]
    PENALTIES = [
        ("Charging", "Charging"),
        ("Cross-checking", "Cross-checking"),
        ("Delay of game", "Delay of game"),
        ("Elbowing", "Elbowing"),
        ("Embellishment", "Embellishment"),
        ("Goaltender interference", "Goaltender interference"),
        ("High-sticking", "High-sticking"),
        ("Hooking", "Hooking"),
        ("Interference", "Interference"),
        ("Roughing", "Roughing"),
        ("Slashing", "Slashing"),
        ("Tripping", "Tripping"),
        ("Unsportsmanlike conduct", "Unsportsmanlike conduct"),
        ("Too many men on the ice", "Too many men on the ice"),
        ("Boarding", "Boarding"),
        ("Fighting", "Fighting"),
    ]

    period = models.CharField(max_length=100, choices=PERIODS)
    severity = models.CharField(max_length=100, choices=PENALTY_SEVERITY)
    length = models.CharField(max_length=100, choices=PENALTY_LENGTH)
    type = models.CharField(max_length=100, choices=PENALTIES)
    timeCommitted = models.CharField(max_length=80)
    # One Player, Many Penalties
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def save(self, *args, **kwargs):
        created = self._state.adding is True
        if created:
            self.addPenaltyMin(self.player.id)
        else:
            oldPenalty = Penalty.objects.get(id=self.id)
            self.removePenaltyMin(oldPenalty.player.id, oldPenalty)
            self.addPenaltyMin(self.player.id)
        super().save(*args, **kwargs)

    def addPenaltyMin(self, playerId):
        playerStats = PlayerStats.objects.get(player__id=playerId)
        playerStats.penaltyMins = playerStats.penaltyMins + int(self.length)
        playerStats.save()

    def removePenaltyMin(self, playerId, oldPenalty):
        playerStats = PlayerStats.objects.get(player__id=playerId)
        playerStats.penaltyMins = playerStats.penaltyMins - int(oldPenalty.length)
        playerStats.save()


def populateDatabases():
    season = Season(name="Winter 2022", numGames=10, seasonActive=True)
    season.save()
    loadDivisions(season)
    loadTeams()
    generateReferees()
    generateScorekeepers()
    generateRinks()


def loadDivisions(season):
    divisions = [
        "WEEKNIGHT B",
        "WEEKNIGHT C",
        "WEEKNIGHT D1",
        "WEEKNIGHT D2",
        "WEEKNIGHT E",
        "WEEKNIGHT TRUE E",
        "WEEKNIGHT NOVICE",
        "OVER 30 WEEKNIGHT",
        "OVER 40 WEEKNIGHT C",
        "OVER 40 WEEKNIGHT D1",
        "OVER 40 WEEKNIGHT D2 NASSAU",
        "OVER 40 WEEKNIGHT D2 SUFFOLK",
        "OVER 40 WEEKNIGHT E",
        "OVER 50 WEEKNIGHT",
        "WEEKEND C1",
        "WEEKEND C2",
        "WEEKEND D1",
        "WEEKEND D2",
        "WEEKEND E",
        "WEEKEND TRUE E",
        "WEEKEND NOVICE",
        "OVER 40 WEEKEND D",
        "OVER 40 WEEKEND E",
    ]

    for i in range(len(divisions)):
        newDivision = Division(name=divisions[i], season=season)
        newDivision.save()


def loadTeams():
    teamDict = {
        "WEEKNIGHT B": [
            "GABAGOOLS",
            "LONG BEACH THUNDER MAJOR",
            "TEAM SHOWERS",
            "BUBBLE BUDDIES",
            "RAW DAWGS",
            "WASHED UP",
            "FNA",
            "COPENHAGEN ROAD SODAS",
        ],
        "WEEKNIGHT C": [
            "ICELANDERS",
            "SAINTS",
            "SPITFIRES BLUE",
            "BEAVERS",
            "HAWKS",
            "DUISLANDERS",
            "TRASH PANDAS",
            "FOREST HC",
        ],
        "WEEKNIGHT D1": [
            "LEFT SHARKS",
            "ASSASSINS",
            "LOCAL 25",
            "PIGEONS",
            "FNA SILVER",
            "DISTINGUISHED JOHNSONS",
            "FOURTH MEAL",
            "IRISH EXIT",
        ],
        "WEEKNIGHT D2": [
            "NO DEKES",
            "OUTLAWS",
            "TORNADOS",
            "ANGRY PIRATES",
            "LONG ISLAND WOLFPACK",
            "QUACKPACK",
            "JAWZ",
            "SALTY BARNACLE MEN",
        ],
        "WEEKNIGHT E": [
            "MINUTEMEN",
            "JUST THE TIP",
            "PRESTIGE WORLDWIDE",
            "LONG ISLAND EXPRESS",
            "SEALS",
        ],
        "WEEKNIGHT TRUE E": [
            "NASSAU RANGERS",
            "THE LOCAL BABYLON NY",
            "ICE RAPTORS",
            "SHARKS AFTER DARK",
            "F PUCKERS",
            "CFD",
            "MIGHTY DRUNKS NORTH",
        ],
        "WEEKNIGHT NOVICE": [
            "ICE HOLES",
            "TRIBE",
            "SHOOTERS",
            "HEMPSTEAD PBA",
            "BREWHAWKS",
            "PIZZA PROFESSOR",
            "TIBURONES",
            "LONG ISLAND WARRIORS",
        ],
        "OVER 30 WEEKNIGHT": [
            "BEERS 30",
            "JACK DANIELS 30",
            "VANQUISH 30",
            "LIGHTNING 30",
        ],
        "OVER 40 WEEKNIGHT C": [
            "ALL CITY 40",
            "WITNESS PROTECTION 40",
            "BEERS 40",
            "FIRE & ICE 40",
        ],
        "OVER 40 WEEKNIGHT D1": [
            "RWG 40",
            "DARK ANGELS 40",
            "HEALTHY SCRATCH 40",
            "TAILGATE 40",
            "HOCKEY UNDERGROUND 40",
        ],
        "OVER 40 WEEKNIGHT D2 NASSAU": [
            "HIGH VOLTAGE 40",
            "SEA CLIFF SURGE 40",
            "MOOSE 40",
            "BLUES 40",
            "OTW 40",
            "SB&G 40",
        ],
        "OVER 40 WEEKNIGHT D2 SUFFOLK": [
            "RENEGADES 40",
            "LI SOUND 40",
            "VERIZON 40",
            "COLONY HARDWARE 40",
            "DUCKS 40",
            "KNIGHTS 40",
            "LI COUGARS 40",
            "AMG GUNNERS 40",
            "OG GRIZZLIES 40",
        ],
        "OVER 40 WEEKNIGHT E": [
            "MATADOR CIGARS 40",
            "OLD TIME BLUES 40",
            "YETI 40",
            "NIGHT CRABS 40",
        ],
        "OVER 50 WEEKNIGHT": [
            "CHEETAHS 50",
            "ICELANDERS 50",
            "ALL CITY 50",
            "ISLAND EMPANADA OLD BOYS 50",
            "SUFFOLK RENEGADES 50",
            "WINTER CLUB 50",
        ],
        "WEEKEND C1": [
            "BAD NEWS BEERS",
            "SPITFIRES RED",
            "EVIL MONKEYS",
            "KOCHS CREW",
            "WILDCATS",
        ],
        "WEEKEND C2": ["BUZZED LIGHTYEARS", "THUNDER", "RAMJETS", "MOOSEHEAD"],
        "WEEKEND D1": [
            "WHISKEY STICKS",
            "MIGHTY DRUNKS",
            "SUAVE THREADS",
            "ROYAL PUCK UPS",
            "WOLFPACK",
            "SUBWAY",
        ],
        "WEEKEND D2": [
            "BARRACUDAS",
            "PUCK ROCKERS",
            "SIEGE",
            "FISHBONES",
            "DANGLIN DAWGZ",
            "SOLAR BEARS HK",
            "MIGHTY DRUNKS SOUTH",
            "WOLVES",
        ],
        "WEEKEND E": [
            "LI STRIPERS",
            "VIPERS",
            "WHACKY DUCKS",
            "BAE",
            "BLUE POINT BREWERY",
            "PHANTOMS",
            "REAPERS",
        ],
        "WEEKEND TRUE E": [
            "ACES",
            "HELLCATS",
            "GARGOYLES",
            "DRAGONS",
            "RIPTIDE",
            "THE BOYS",
            "HAMMERHEADS",
        ],
        "WEEKEND NOVICE": [
            "SKATEFUL DEAD",
            "RINK REAPERS",
            "SUICIDE SQUAD",
            "CHAOS",
            "THIN ICE",
        ],
        "OVER 40 WEEKEND D": [
            "AVALANCHE 40",
            "EAGLES 40",
            "KING CRABS 40",
            "SAINTS 40",
        ],
        "OVER 40 WEEKEND E": [
            "CEMENT SKATES 40",
            "BULLDOGS 40",
            "MAVENS 40",
            "LI AMERICANS 40",
            "K-STARS 40",
            "CROWS 40",
            "MUSTANGS 40",
        ],
    }

    for key in teamDict:
        division = Division.objects.get(name=key)
        for i in range(len(teamDict[key])):
            newTeam = Team(name=teamDict[key][i], division=division)
            newTeam.save()
            generatePlayers(newTeam)


def generatePlayers(team):
    teamSize = random.randint(10, 15)
    posList = ["F", "D"]
    teamRoster = []
    for i in range(teamSize):
        player = [
            names.get_first_name(),
            names.get_last_name(),
            random.randint(0, 99),
            random.choice(posList),
        ]
        teamRoster.append(player)
    for i in range(len(teamRoster)):
        newPlayer = Player(
            firstName=teamRoster[i][0],
            lastName=teamRoster[i][1],
            jerseyNumber=teamRoster[i][2],
            position=teamRoster[i][3],
            team=team,
        )
        newPlayer.save()


def generateReferees():
    for i in range(20):
        newRef = Referee(
            name=names.get_full_name(),
            phoneNumber=str(random.randint(1111111111, 9999999999)),
            email="sample@gmail.com",
        )
        newRef.save()


def generateScorekeepers():
    for i in range(20):
        newScorekeeper = Scorekeeper(
            name=names.get_full_name(),
            phoneNumber=str(random.randint(1111111111, 9999999999)),
            email="sample@gmail.com",
        )
        newScorekeeper.save()


def generateRinks():
    rinkList = [
        {
            "name": "BETHPAGE",
            "streetAddress": "1001 STEWART AVE",
            "city": "Bethpage",
            "state": "NY",
            "zip": "11714",
            "phoneNumber": "516-433-7465",
        },
        {
            "name": "CANTIAGUE",
            "streetAddress": "480 WEST JOHN ST",
            "city": "Hicksville",
            "state": "NY",
            "zip": "11801",
            "phoneNumber": "5165717056",
        },
        {
            "name": "CHRISTOPHER MORLEY",
            "streetAddress": "500 SEARINGTOWN RD",
            "city": "Roslyn",
            "state": "NY",
            "zip": "11576",
            "phoneNumber": "516-571-8120",
        },
        {
            "name": "Dix Hills",
            "streetAddress": "575 VANDERBILT PARKWAY",
            "city": "Dix Hills",
            "state": "NY",
            "zip": "11746",
            "phoneNumber": "6314625883",
        },
        {
            "name": "EISENHOWER",
            "streetAddress": "200 MERRICK AVE",
            "city": "East Meadow",
            "state": "NY",
            "zip": "11554",
            "phoneNumber": "5164410070",
        },
        {
            "name": "Freeport",
            "streetAddress": "130 E. MERRICK RD",
            "city": "Freeport",
            "state": "NY",
            "zip": "11520",
            "phoneNumber": "5163772314",
        },
        {
            "name": "ICELAND",
            "streetAddress": "3345 HILLSIDE AVE",
            "city": "New Hyde Park",
            "state": "NY",
            "zip": "11040",
            "phoneNumber": "5167461100",
        },
        {
            "name": "LONG BEACH",
            "streetAddress": "150 W BAY DR",
            "city": "Long Beach",
            "state": "NY",
            "zip": "11561",
            "phoneNumber": "5167057385",
        },
        {
            "name": "NEWBRIDGE",
            "streetAddress": "2600 NEWBRIDGE RD",
            "city": "Bellmore",
            "state": "NY",
            "zip": "11710",
            "phoneNumber": "5167836181",
        },
        {
            "name": "PARKWOOD",
            "streetAddress": "65 ARRANDALE AVE",
            "city": "Great Neck",
            "state": "NY",
            "zip": "11024",
            "phoneNumber": "5164874673",
        },
        {
            "name": "SUPERIOR",
            "streetAddress": "270 INDIAN HEAD RD",
            "city": "Kings Park",
            "state": "NY",
            "zip": "11754",
            "phoneNumber": "6312693900",
        },
        {
            "name": "Syosset Iceworks",
            "streetAddress": "175 UNDERHILL BLVD",
            "city": "Syosset",
            "state": "NY",
            "zip": "11791",
            "phoneNumber": "5164962277",
        },
        {
            "name": "SYOSSET WOODBURY PARK",
            "streetAddress": "7800 JERICHO TURNPIKE",
            "city": "Woodbury",
            "state": "NY",
            "zip": "11797",
            "phoneNumber": "5166775990",
        },
        {
            "name": "THE RINX",
            "streetAddress": "660 TERRY RD",
            "city": "Hauppauge",
            "state": "NY",
            "zip": "11788",
            "phoneNumber": "6312323222",
        },
        {
            "name": "UBS ARENA",
            "streetAddress": "2400 HEMPSTEAD TURNPIKE",
            "city": "Elmont",
            "state": "NY",
            "zip": "11003",
            "phoneNumber": "7182175477",
        },
    ]
    for i in range(len(rinkList)):
        rink = Rink(
            name=rinkList[i]["name"],
            streetAddress=rinkList[i]["streetAddress"],
            city=rinkList[i]["city"],
            state=rinkList[i]["state"],
            zip=rinkList[i]["zip"],
            phoneNumber=rinkList[i]["phoneNumber"],
        )
        rink.save()
