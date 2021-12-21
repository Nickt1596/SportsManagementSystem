# Form for scorekeeper entering in game results
# 1. Enter in the box score, goals per period for each team
# 2. Then you press the next button which submits that, and enters individual goals
# TODO Create a "Goal" Model to store a goal
from django.forms import *
from django import forms
from .models import *


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
