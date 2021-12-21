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


# Models Relationships
# One Season can have Many Divisions
# One Division can have many teams
# One team can belong to only one division
# One player can belong to many teams


# Create your models here.

# Will need a create new season form with some options
# Import Prior Season Teams/Divisions
# Season Manager portal
# Portal to Add Team/Add Division/Change Team Division
# A Season can have many Divisions/Teams
class Season(models.Model):
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=50)
    numGames = models.CharField(max_length=3)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


# A division can belong to many seasons
class Division(models.Model):
    name = models.CharField(max_length=50)
    seasons = models.ManyToManyField(Season, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


# A team can belong to many seasons
class Team(models.Model):
    name = models.CharField(max_length=80)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        created = self._state.adding is True
        if created:
            super().save(*args, **kwargs)
            team = Team.objects.get(id=self.id)
            teamStats = TeamStats(team=team)
            teamStats.save()
        else:
            super().save(*args, **kwargs)


class TeamStats(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    regWins = models.IntegerField(default=0)
    regLoses = models.IntegerField(default=0)
    otWins = models.IntegerField(default=0)
    otLoses = models.IntegerField(default=0)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.team.name


class Player(models.Model):
    firstName = models.CharField(max_length=80)
    lastName = models.CharField(max_length=80)
    jerseyNumber = models.IntegerField(default=0)
    position = models.CharField(max_length=80)
    captain = models.BooleanField(default=False)
    altCaptain = models.BooleanField(default=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.firstName + ' ' + self.lastName

    def save(self, *args, **kwargs):
        created = self._state.adding is True
        if created:
            super().save(*args, **kwargs)
            player = Player.objects.get(id=self.id)
            playerStats = PlayerStats(player=player, team=self.team)
            playerStats.save()
        else:
            super().save(*args, **kwargs)


class PlayerStats(models.Model):
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    gamesPlayed = models.IntegerField(default=0)
    playoffEligible = models.BooleanField(default=False)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.player.firstName + ' ' + self.player.lastName


class Scorekeeper(models.Model):
    name = models.CharField(max_length=80)
    phoneNumber = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Referee(models.Model):
    name = models.CharField(max_length=80)
    phoneNumber = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Rink(models.Model):
    name = models.CharField(max_length=80)
    streetAddress = models.CharField(max_length=150)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80)
    zip = models.CharField(max_length=80)
    phoneNumber = models.CharField(max_length=80)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


# When Deleting an Ice Slot, we need to check if a game currently has that Ice Slot assigned
# If it does, we change the Game Ice Slot back to null
class IceSlot(models.Model):
    rink = models.ForeignKey(Rink, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    available = models.BooleanField(default=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.rink.name + ' ' + str(self.date) + ' ' + str(self.time)


# When Deleting a Game we need to change the ice slot back to available
# When changing the ice slot for a Game, we need to change the original ice slot back to available
class Game(models.Model):
    homeTeam = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name='Home_Team')
    awayTeam = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name='Away_Team')
    iceSlot = models.ForeignKey(IceSlot, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={'available': True})
    scorekeeper = models.ForeignKey(Scorekeeper, on_delete=models.CASCADE, blank=True, null=True)
    referees = models.ManyToManyField(Referee, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.homeTeam.name + ' vs ' + self.awayTeam.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        iceSlot = IceSlot.objects.get(id=self.iceSlot.id)
        iceSlot.available = False
        iceSlot.save()


def loadDivisions():
    divisions = [
        'WEEKNIGHT B',
        'WEEKNIGHT C',
        'WEEKNIGHT D1',
        'WEEKNIGHT D2',
        'WEEKNIGHT E',
        'WEEKNIGHT TRUE E',
        'WEEKNIGHT NOVICE',
        'OVER 30 WEEKNIGHT',
        'OVER 40 WEEKNIGHT C',
        'OVER 40 WEEKNIGHT D1',
        'OVER 40 WEEKNIGHT D2 NASSAU',
        'OVER 40 WEEKNIGHT D2 SUFFOLK',
        'OVER 40 WEEKNIGHT E',
        'OVER 50 WEEKNIGHT',
        'WEEKEND C1',
        'WEEKEND C2',
        'WEEKEND D1',
        'WEEKEND D2',
        'WEEKEND E',
        'WEEKEND TRUE E',
        'WEEKEND NOVICE',
        'OVER 40 WEEKEND D',
        'OVER 40 WEEKEND E',
    ]

    for i in range(len(divisions)):
        newDivision = Division(name=divisions[i])
        newDivision.save()


def loadTeams():
    teamDict = {
        'WEEKNIGHT B': ['GABAGOOLS',
                        'LONG BEACH THUNDER MAJOR',
                        'TEAM SHOWERS',
                        'BUBBLE BUDDIES',
                        'RAW DAWGS',
                        'WASHED UP',
                        'FNA',
                        'COPENHAGEN ROAD SODAS'],
        'WEEKNIGHT C': ['ICELANDERS',
                        'SAINTS',
                        'SPITFIRES BLUE',
                        'BEAVERS',
                        'HAWKS',
                        'DUISLANDERS',
                        'TRASH PANDAS',
                        'FOREST HC'],
        'WEEKNIGHT D1': ['LEFT SHARKS',
                         'ASSASSINS',
                         'LOCAL 25',
                         'PIGEONS',
                         'FNA SILVER',
                         'DISTINGUISHED JOHNSONS',
                         'FOURTH MEAL',
                         'IRISH EXIT'],
        'WEEKNIGHT D2': ['NO DEKES',
                         'OUTLAWS',
                         'TORNADOS',
                         'ANGRY PIRATES',
                         'LONG ISLAND WOLFPACK',
                         'QUACKPACK',
                         'JAWZ',
                         'SALTY BARNACLE MEN'],
        'WEEKNIGHT E': ['MINUTEMEN',
                        'JUST THE TIP',
                        'PRESTIGE WORLDWIDE',
                        'LONG ISLAND EXPRESS',
                        'SEALS'],
        'WEEKNIGHT TRUE E': ['NASSAU RANGERS',
                             'THE LOCAL BABYLON NY',
                             'ICE RAPTORS',
                             'SHARKS AFTER DARK',
                             'F PUCKERS',
                             'CFD',
                             'MIGHTY DRUNKS NORTH'],
        'WEEKNIGHT NOVICE': ['ICE HOLES',
                             'TRIBE',
                             'SHOOTERS',
                             'HEMPSTEAD PBA',
                             'BREWHAWKS',
                             'PIZZA PROFESSOR',
                             'TIBURONES',
                             'LONG ISLAND WARRIORS'],
        'OVER 30 WEEKNIGHT': ['BEERS 30',
                              'JACK DANIELS 30',
                              'VANQUISH 30',
                              'LIGHTNING 30'],
        'OVER 40 WEEKNIGHT C': ['ALL CITY 40',
                                'WITNESS PROTECTION 40',
                                'BEERS 40',
                                'FIRE & ICE 40'],
        'OVER 40 WEEKNIGHT D1': ['RWG 40',
                                 'DARK ANGELS 40',
                                 'HEALTHY SCRATCH 40',
                                 'TAILGATE 40',
                                 'HOCKEY UNDERGROUND 40'],
        'OVER 40 WEEKNIGHT D2 NASSAU': ['HIGH VOLTAGE 40',
                                        'SEA CLIFF SURGE 40',
                                        'MOOSE 40',
                                        'BLUES 40',
                                        'OTW 40',
                                        'SB&G 40'],
        'OVER 40 WEEKNIGHT D2 SUFFOLK': ['RENEGADES 40',
                                         'LI SOUND 40',
                                         'VERIZON 40',
                                         'COLONY HARDWARE 40',
                                         'DUCKS 40',
                                         'KNIGHTS 40',
                                         'LI COUGARS 40',
                                         'AMG GUNNERS 40',
                                         'OG GRIZZLIES 40'],
        'OVER 40 WEEKNIGHT E': ['MATADOR CIGARS 40',
                                'OLD TIME BLUES 40',
                                'YETI 40',
                                'NIGHT CRABS 40'],
        'OVER 50 WEEKNIGHT': ['CHEETAHS 50',
                              'ICELANDERS 50',
                              'ALL CITY 50',
                              'ISLAND EMPANADA OLD BOYS 50',
                              'SUFFOLK RENEGADES 50',
                              'WINTER CLUB 50'],
        'WEEKEND C1': ['BAD NEWS BEERS',
                       'SPITFIRES RED',
                       'EVIL MONKEYS',
                       'KOCHS CREW',
                       'WILDCATS'],
        'WEEKEND C2': ['BUZZED LIGHTYEARS',
                       'THUNDER',
                       'RAMJETS',
                       'MOOSEHEAD'],
        'WEEKEND D1': ['WHISKEY STICKS',
                       'MIGHTY DRUNKS',
                       'SUAVE THREADS',
                       'ROYAL PUCK UPS',
                       'WOLFPACK',
                       'SUBWAY'],
        'WEEKEND D2': ['BARRACUDAS',
                       'PUCK ROCKERS',
                       'SIEGE',
                       'FISHBONES',
                       'DANGLIN DAWGZ',
                       'SOLAR BEARS HK',
                       'MIGHTY DRUNKS SOUTH',
                       'WOLVES'],
        'WEEKEND E': ['LI STRIPERS',
                      'VIPERS',
                      'WHACKY DUCKS',
                      'BAE',
                      'BLUE POINT BREWERY',
                      'PHANTOMS',
                      'REAPERS'],
        'WEEKEND TRUE E': ['ACES',
                           'HELLCATS',
                           'GARGOYLES',
                           'DRAGONS',
                           'RIPTIDE',
                           'THE BOYS',
                           'HAMMERHEADS'],
        'WEEKEND NOVICE': ['SKATEFUL DEAD',
                           'RINK REAPERS',
                           'SUICIDE SQUAD',
                           'CHAOS',
                           'THIN ICE'],
        'OVER 40 WEEKEND D': ['AVALANCHE 40',
                              'EAGLES 40',
                              'KING CRABS 40',
                              'SAINTS 40'],
        'OVER 40 WEEKEND E': ['CEMENT SKATES 40',
                              'BULLDOGS 40',
                              'MAVENS 40',
                              'LI AMERICANS 40',
                              'K-STARS 40',
                              'CROWS 40',
                              'MUSTANGS 40']
    }

    for key in teamDict:
        division = Division.objects.get(name=key)
        print(key)
        for i in range(len(teamDict[key])):
            print(teamDict[key][i])
            newTeam = Team(name=teamDict[key][i], division=division)
            newTeam.save()
            team = Team.objects.get(name=teamDict[key][i])
            teamStats = TeamStats(team=team)
            teamStats.save()
            # Going to populate Team With Players Here
            generatePlayers(team)


def generatePlayers(team):
    teamSize = random.randint(10, 15)
    posList = ['F', 'D']
    teamRoster = []
    for i in range(teamSize):
        player = [names.get_first_name(), names.get_last_name(), random.randint(0, 99), random.choice(posList)]
        teamRoster.append(player)
    for i in range(len(teamRoster)):
        newPlayer = Player(firstName=teamRoster[i][0], lastName=teamRoster[i][1],
                           jerseyNumber=teamRoster[i][2], position=teamRoster[i][3], team=team)
        newPlayer.save()
        newPlayerStats = PlayerStats(player=newPlayer, team=team)
        newPlayerStats.save()


def generateReferees():
    for i in range(20):
        newRef = Referee(name=names.get_full_name(),
                         phoneNumber=str(random.randint(1111111111, 9999999999)),
                         email='sample@gmail.com')
        newRef.save()


def generateScorekeepers():
    for i in range(20):
        newScorekeeper = Scorekeeper(name=names.get_full_name(),
                         phoneNumber=str(random.randint(1111111111, 9999999999)),
                         email='sample@gmail.com')
        newScorekeeper.save()
