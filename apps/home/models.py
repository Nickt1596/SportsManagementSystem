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
    currentSeason = models.BooleanField(default=False)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


# A division can belong to many seasons
class Division(models.Model):
    name = models.CharField(max_length=50)
    seasons = models.ManyToManyField(Season, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


# A team can belong to many seasons
class Team(models.Model):
    name = models.CharField(max_length=80)
    division = models.ForeignKey(Division, blank=True, null=True, on_delete=models.CASCADE)
    seasons = models.ManyToManyField(Season, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
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
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)
    regWins = models.IntegerField(default=0)
    regLoses = models.IntegerField(default=0)
    otWins = models.IntegerField(default=0)
    otLoses = models.IntegerField(default=0)
    ties = models.IntegerField(default=0)
    season = models.ForeignKey(Season, blank=True, null=True, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.team.name


class Player(models.Model):
    firstName = models.CharField(max_length=80)
    lastName = models.CharField(max_length=80)
    jerseyNumber = models.CharField(max_length=3)
    # jerseyNumber = models.IntegerField(default=0)
    position = models.CharField(max_length=80, blank=True, null=True)
    captain = models.BooleanField(default=False)
    altCaptain = models.BooleanField(default=False)
    team = models.ForeignKey(Team, blank=True, null=True, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return '#' + self.jerseyNumber + ' ' + self.firstName + '. ' + self.lastName

        # return '#' + self.jerseyNumber + ' ' + self.firstName[0] + '. ' + self.lastName

    def save(self, *args, **kwargs):
        created = self._state.adding is True
        if created:
            if len(self.firstName) != 0 and len(self.lastName) != 0 and len(
                    self.jerseyNumber) != 0 and self.team is not None:
                print('Valid Player Object')
                super().save(*args, **kwargs)
                player = Player.objects.get(id=self.id)
                playerStats = PlayerStats(player=player)
                playerStats.save()
            else:
                print('Invalid Player Object')
        else:
            super().save(*args, **kwargs)


class PlayerStats(models.Model):
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    gamesPlayed = models.IntegerField(default=0)
    playoffEligible = models.BooleanField(default=False)
    player = models.ForeignKey(Player, blank=True, null=True, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, blank=True, null=True, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.player.firstName + ' ' + self.player.lastName


class Scorekeeper(models.Model):
    name = models.CharField(max_length=80)
    phoneNumber = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Referee(models.Model):
    name = models.CharField(max_length=80)
    phoneNumber = models.CharField(max_length=80)
    email = models.CharField(max_length=80)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
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
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


# When Deleting an Ice Slot, we need to check if a game currently has that Ice Slot assigned
# If it does, we change the Game Ice Slot back to null
class IceSlot(models.Model):
    rink = models.ForeignKey(Rink, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    available = models.BooleanField(default=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.rink.name + ' ' + str(self.date) + ' ' + str(self.time)


# When Deleting a Game we need to change the ice slot back to available
# When changing the ice slot for a Game, we need to change the original ice slot back to available
class Game(models.Model):
    homeTeam = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name='Home_Team')
    awayTeam = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name='Away_Team')
    iceSlot = models.ForeignKey(IceSlot, on_delete=models.CASCADE, blank=True, null=True,
                                limit_choices_to={'available': True})
    scorekeeper = models.ForeignKey(Scorekeeper, on_delete=models.CASCADE, blank=True, null=True)
    referees = models.ManyToManyField(Referee, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.homeTeam.name + ' vs ' + self.awayTeam.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        iceSlot = IceSlot.objects.get(id=self.iceSlot.id)
        iceSlot.available = False
        iceSlot.save()


class Goal(models.Model):
    PERIODS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('OT', 'OT')
    ]

    goalScorer = models.ForeignKey(PlayerStats, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='Goal_Scorer')
    assistPrimary = models.ForeignKey(PlayerStats, on_delete=models.CASCADE, blank=True, null=True,
                                      related_name='Primary_Assist')
    assistSecondary = models.ForeignKey(PlayerStats, on_delete=models.CASCADE, blank=True, null=True,
                                        related_name='Secondary_Assist')
    period = models.CharField(max_length=100, choices=PERIODS)
    timeScored = models.CharField(max_length=80)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


class Penalty(models.Model):
    PERIODS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('OT', 'OT')
    ]
    PENALTY_SEVERITY = [
        ('Minor', 'Minor'),
        ('Double Minor', 'Double Minor'),
        ('Major', 'Major'),
        ('Game Misconduct', 'Game Misconduct'),
        ('Match', 'Match')
    ]
    PENALTY_LENGTH = [
        ('2', '2'),
        ('4', '4'),
        ('5', '5'),
        ('10', '10')
    ]
    PENALTIES = [
        ('Charging', 'Charging'),
        ('Cross-checking', 'Cross-checking'),
        ('Delay of game', 'Delay of game'),
        ('Elbowing', 'Elbowing'),
        ('Embellishment', 'Embellishment'),
        ('Goaltender interference', 'Goaltender interference'),
        ('High-sticking', 'High-sticking'),
        ('Hooking', 'Hooking'),
        ('Interference', 'Interference'),
        ('Roughing', 'Roughing'),
        ('Slashing', 'Slashing'),
        ('Tripping', 'Tripping'),
        ('Unsportsmanlike conduct', 'Unsportsmanlike conduct'),
        ('Too many men on the ice', 'Too many men on the ice'),
        ('Boarding', 'Boarding'),
        ('Fighting', 'Fighting'),
    ]

    period = models.CharField(max_length=100, choices=PERIODS)
    severity = models.CharField(max_length=100, choices=PENALTY_SEVERITY)
    length = models.CharField(max_length=100, choices=PENALTY_LENGTH)
    type = models.CharField(max_length=100, choices=PENALTIES)
    timeCommitted = models.CharField(max_length=80)
    player = models.ForeignKey(PlayerStats, blank=True, null=True, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)


class GameResult(models.Model):
    WIN_TYPES = [
        ('Regulation', 'REG'),
        ('Overtime', 'OT'),
        ('Shootout', 'SO'),
        ('Tie', 'TIE'),
    ]
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True, )
    winningTeam = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name='Winning_Team')
    losingTeam = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True, related_name='Losing_Team')
    winType = models.CharField(max_length=100, choices=WIN_TYPES)
    winnerScore = models.IntegerField(default=0)
    loserScore = models.IntegerField(default=0)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.game.homeTeam.name + ' vs ' + self.game.awayTeam.name + ' Result'


class TempGameResults(models.Model):
    WIN_TYPES = [
        ('Regulation', 'REG'),
        ('Overtime', 'OT'),
        ('Shootout', 'SO'),
        ('Tie', 'TIE'),
    ]
    # Will Hold from Step 1 our select game
    # game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True, unique=True)
    # Will hold our Temp Players who played from both teams
    game = models.OneToOneField(Game, on_delete=models.CASCADE, blank=True, null=True, unique=True)
    homePlayers = models.ManyToManyField(Player, blank=True, related_name='Home_Players_Temp')
    awayPlayers = models.ManyToManyField(Player, blank=True, related_name='Away_Players_Temp')
    winningTeam = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name='Winning_Team_Temp')
    losingTeam = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='Losing_Team_Temp')
    tempGoals = models.ManyToManyField(Goal, blank=True, related_name='Goals_Temp')
    tempPenalties = models.ManyToManyField(Penalty, blank=True, related_name='Penalties_Temp')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.game.homeTeam.name + ' vs ' + self.game.awayTeam.name + ' Temp Result'

    # def save(self, *args, **kwargs):
    #     created = self._state.adding is True
    #     super().save(*args, **kwargs)
    #     if created:
    #         super().save(*args, **kwargs)
    # homePlayers = Player.objects.filter(team__id=self.game.homeTeam.id)
    # awayTeamPlayers = Player.objects.filter(team__id=self.game.awayTeam.id)
    # self.homePlayers.set(homePlayers)
    # self.awayPlayers.set(awayTeamPlayers)
    # super().save(*args, **kwargs)


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


# For when a new season is added, and they opt to import last seasons data
def seasonImport(season):
    currentSeason = Season.objects.filter(currentSeason=True)
    divisions = Division.objects.filter(seasons__in=currentSeason).values()
    teams = Team.objects.filter(seasons__in=currentSeason).values()
    playerStats = PlayerStats.objects.filter(season__in=currentSeason).values()
    teamStats = TeamStats.objects.filter(season__in=currentSeason).values()

    for division in divisions:
        updateDivision = Division.objects.get(name=division['name'])
        updateDivision.seasons.add(season)
        updateDivision.save()

    for team in teams:
        updateTeam = Team.objects.get(name=team['name'])
        updateTeam.seasons.add(season)
        updateTeam.save()

    for playerStat in playerStats:
        player = Player.objects.get(id=playerStat['player_id'])
        newPlayerStat = PlayerStats(player=player, season=season)
        newPlayerStat.save()

    for teamStat in teamStats:
        team = Team.objects.get(id=teamStat['team_id'])
        newTeamStat = TeamStats(team=team, season=season)
        newTeamStat.save()
