# Form for scorekeeper entering in game results
# 1. Enter in the box score, goals per period for each team
# 2. Then you press the next button which submits that, and enters individual goals
# TODO Create a "Goal" Model to store a goal
from django.forms import *
from django import forms
from .models import *


class GameResultForm(ModelForm):
    class Meta:
        model = GameResult
        fields = {'winningTeam', 'losingTeam', 'winType', 'winnerScore', 'loserScore'}
        labels = {
            'winningTeam': 'Winning Team',
            'losingTeam': 'Losing Team',
            'winType': 'Win Type',
            'winnerScore': 'Winner Score',
            'loserScore': 'Loser Score',
        }
        widgets = {
            'winningTeam': Select(attrs={'class': 'form-control', 'id': 'winningTeam'}),
            'losingTeam': Select(attrs={'class': 'form-control', 'id': 'losingTeam'}),
            'winType': Select(attrs={'class': 'form-control', 'id': 'winType'}),
            'winnerScore': NumberInput(attrs={'class': 'form-control', 'type': 'number', 'id': 'winnerScore'}),
            'loserScore': NumberInput(attrs={'class': 'form-control', 'type': 'number', 'id': 'loserScore'})
        }

    def __init__(self, *args, **kwargs):
        teams = kwargs.pop('teams')
        super(GameResultForm, self).__init__(*args, **kwargs)
        self.fields['winningTeam'].queryset = teams
        self.fields['losingTeam'].queryset = teams
        # self.fields['period'].label = 'Period'
        # self.fields['severity'].label = 'Severity'
        # self.fields['length'].label = 'Length'
        # self.fields['type'].label = 'Type'
        # self.fields['timeCommitted'].label = 'Time'


class PenaltyForm(ModelForm):
    class Meta:
        model = Penalty
        fields = {'period', 'severity', 'length', 'type', 'timeCommitted', 'player'}
        labels = {
            'period': 'Period',
            'severity': 'Severity',
            'length': 'Length',
            'type': 'Type',
            'timeCommitted': 'Time',
            'player': 'Player'
        }
        widgets = {
            'period': Select(attrs={'class': 'form-control', 'id': 'penaltyPeriod'}),
            'severity': Select(attrs={'class': 'form-control', 'id': 'severity'}),
            'length': Select(attrs={'class': 'form-control', 'id': 'length'}),
            'type': Select(attrs={'class': 'form-control', 'id': 'type'}),
            'timeCommitted': TextInput(attrs={'class': 'form-control', 'placeholder': 'Time', 'id': 'timeCommitted'}),
            'player': Select(attrs={'class': 'form-control', 'id': 'player'})
        }

    def __init__(self, *args, **kwargs):
        players = kwargs.pop('players')
        super(PenaltyForm, self).__init__(*args, **kwargs)
        self.fields['player'].queryset = players
        self.fields['period'].label = 'Period'
        self.fields['severity'].label = 'Severity'
        self.fields['length'].label = 'Length'
        self.fields['type'].label = 'Type'
        self.fields['timeCommitted'].label = 'Time'
        self.fields['player'].label = 'Player'


PenaltyFormSet = modelformset_factory(
    model=Penalty,
    form=PenaltyForm,
    extra=1
)


class GoalForm(ModelForm):
    class Meta:
        model = Goal
        fields = {'goalScorer', 'assistPrimary', 'assistSecondary', 'period', 'timeScored'}
        label = {
            'goalScorer': 'Goal Scorer',
            'assistPrimary': 'Primary Assist',
            'assistSecondary': 'Secondary Assist',
            'period': 'Period',
            'timeScored': 'Time Scored'
        }
        widgets = {
            'goalScorer': Select(attrs={'class': 'form-control', 'id': 'goalScorer'}),
            'assistPrimary': Select(attrs={'class': 'form-control', 'id': 'assistPrimary'}),
            'assistSecondary': Select(attrs={'class': 'form-control', 'id': 'assistSecondary'}),
            'period': Select(attrs={'class': 'form-control', 'id': 'goalPeriod'}),
            'timeScored': TextInput(attrs={'class': 'form-control', 'placeholder': 'Time', 'id': 'timeScored'})
        }

    def __init__(self, *args, **kwargs):
        players = kwargs.pop('players')
        super(GoalForm, self).__init__(*args, **kwargs)
        self.fields['goalScorer'].queryset = players
        self.fields['assistPrimary'].queryset = players
        self.fields['assistSecondary'].queryset = players
        self.fields['goalScorer'].label = 'Goal Scorer'
        self.fields['assistPrimary'].label = 'Primary Assist'
        self.fields['assistSecondary'].label = 'Secondary Assist'
        self.fields['period'].label = 'Period'
        self.fields['timeScored'].label = 'Time Scored'
    #
    #     self.fields['goalScorer'].widget.attrs.update({
    #         ''
    #     })


GoalFormSet = modelformset_factory(
    model=Goal,
    form=GoalForm,
    extra=1
)


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = {'firstName', 'lastName', 'jerseyNumber'}

    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control',
                                       'type': 'text',
                                       'placeholder': 'placeholder'})


PlayerFormSet = modelformset_factory(
    Player,
    fields={'firstName', 'lastName', 'jerseyNumber'},
    extra=1,
    widgets={
        'firstName': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name',
            'id': 'firstName'
        }),
        'lastName': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name',
            'id': 'lastName'
        }),
        'jerseyNumber': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Jersey #',
            'id': 'jerseyNumber'
        }),

    }
)


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['homeTeam', 'awayTeam', 'iceSlot', 'scorekeeper', 'referees']
        labels = {
            'homeTeam': 'Home Team',
            'awayTeam': 'Away Team',
            'iceSlot': 'Ice Slot',
            'scorekeeper': 'Score Keeper',
        }

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields['iceSlot'].choices = IceSlot.objects.filter(available=True)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


GameFormSet = modelformset_factory(
    Game,
    fields=('homeTeam', 'awayTeam', 'iceSlot', 'scorekeeper', 'referees'),
    labels={
        'homeTeam': 'Home Team',
        'awayTeam': 'Away Team',
        'iceSlot': 'Ice Slot',
        'scorekeeper': 'Scorekeeper',
        'referees': 'Referees'
    },
    extra=1,
    widgets={
        'homeTeam': Select(attrs={
            'class': 'form-control',
            'id': 'homeTeam'
        }),
        'awayTeam': Select(attrs={
            'class': 'form-control',
            'id': 'awayTeam'
        }),
        'iceSlot': Select(attrs={
            'class': 'form-control',
            'id': 'iceSlot'
        }),
        'scorekeeper': Select(attrs={
            'class': 'form-control',
            'id': 'scorekeeper'
        }),
        # 'referees': Select(attrs={
        #     'class': 'form-control',
        #     'id': 'referees'
        # })
    }

)


class IceSlotForm(ModelForm):
    class Meta:
        model = IceSlot
        fields = ['rink', 'date', 'time']
        labels = {
            'rink': 'Rink',
            'date': 'Date',
            'time': 'Time',
        }

    def __init__(self, *args, **kwargs):
        super(IceSlotForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


IceSlotFormSet = modelformset_factory(
    IceSlot,
    fields=('rink', 'date', 'time'),
    labels={
        'rink': 'Rink',
        'date': 'Date',
        'time': 'Time',
    },
    extra=1,
    widgets={
        'date': forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'iceSlotDate',
            'value': date.today()
        }),
        'time': forms.TimeInput(attrs={
            'class': 'form-control',
            'type': 'time',
            'id': 'iceSlotTime',
            'value': '20:30:00'
        }),
        'rink': Select(attrs={
            'class': 'form-control',
            'id': 'iceSlotRink'
        }),
    }
)


class SeasonForm(ModelForm):
    class Meta:
        model = Season
        fields = ['name', 'startDate', 'endDate', 'numGames']
        labels = {
            'name': 'Season Name',
            'startDate': 'Start Date',
            'endDate': 'End Date',
            'numGames': '# of Games',
        }
        widgets = {
            'startDate': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'seasonStartDate',
                'value': date.today()
            }),
            'endDate': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'seasonEndDate',
                'value': date.today()
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'seasonName'
            }),
            'numGames': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'seasonNumGames'
            }),
        }

    # def __init__(self, *args, **kwargs):
    #     super(SeasonForm, self).__init__(*args, **kwargs)
    #
    #     for name, field in self.fields.items():
    #         field.widget.attrs.update({'class': 'form-control'})
    #
    #     self.fields['startDate'].widget.attrs.update({'type': 'date', 'id': 'seasonStartDate', 'value': date.today()})
    #     self.fields['endDate'].widget.attrs.update({'type': 'date', 'id': 'seasonStartDate', 'value': date.today()})
