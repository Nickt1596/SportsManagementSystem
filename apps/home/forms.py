# Form for scorekeeper entering in game results
# 1. Enter in the box score, goals per period for each team
# 2. Then you press the next button which submits that, and enters individual goals
from django.forms import *
from django import forms
from .models import *


class GameResultRosterForm(ModelForm):
    class Meta:
        model = Player
        fields = {"firstName", "lastName", "jerseyNumber"}

    def __init__(self, *args, **kwargs):
        super(GameResultRosterForm, self).__init__(*args, **kwargs)
        self.fields["firstName"].label = "First Name"
        self.fields["firstName"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First Name",
                "id": "firstName",
                "required": "required",
            }
        )
        self.fields["lastName"].label = "Last Name"
        self.fields["lastName"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Last Name",
                "id": "lastName",
                "required": "required",
            }
        )
        self.fields["jerseyNumber"].label = "Jersey #"
        self.fields["jerseyNumber"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Jersey #",
                "id": "jerseyNumber",
                "required": "required",
            }
        )


GameResultRosterFormSet = modelformset_factory(
    model=Player, form=GameResultRosterForm, extra=1
)


class GameResultQuickForm(ModelForm):
    class Meta:
        model = GameResult
        fields = {"winningTeam", "losingTeam", "winnerScore", "loserScore", "winType"}

    def __init__(self, *args, **kwargs):
        teams = kwargs.pop("teams")
        super(GameResultQuickForm, self).__init__(*args, **kwargs)
        self.fields["winningTeam"].label = "Winning Team"
        self.fields["winningTeam"].widget = Select(
            attrs={"class": "form-control", "id": "winningTeam", "required": "required"}
        )
        self.fields["winningTeam"].queryset = teams
        self.fields["losingTeam"].label = "Losing Team"
        self.fields["losingTeam"].widget = Select(
            attrs={"class": "form-control", "id": "losingTeam", "required": "required"}
        )
        self.fields["losingTeam"].queryset = teams
        self.fields["winnerScore"].label = "Winner Score"
        self.fields["winnerScore"].widget = NumberInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "id": "winnerScore",
                "required": "required",
            }
        )
        self.fields["loserScore"].label = "Loser Score"
        self.fields["loserScore"].widget = NumberInput(
            attrs={
                "class": "form-control",
                "type": "number",
                "id": "loserScore",
                "required": "required",
            }
        )
        self.fields["winType"].label = "Win Type"
        self.fields["winType"].widget = Select(
            attrs={"class": "form-control", "id": "winType", "required": "required"}
        )
        self.fields["winType"].choices = GameResult.WIN_TYPES


class PenaltyForm(ModelForm):
    class Meta:
        model = Penalty
        fields = {"period", "severity", "length", "type", "timeCommitted", "player"}
        labels = {
            "period": "Period",
            "severity": "Severity",
            "length": "Length",
            "type": "Type",
            "timeCommitted": "Time",
            "player": "Player",
        }
        widgets = {
            "period": Select(attrs={"class": "form-control", "id": "penaltyPeriod"}),
            "severity": Select(attrs={"class": "form-control", "id": "severity"}),
            "length": Select(attrs={"class": "form-control", "id": "length"}),
            "type": Select(attrs={"class": "form-control", "id": "type"}),
            "timeCommitted": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Time",
                    "id": "timeCommitted",
                }
            ),
            "player": Select(attrs={"class": "form-control", "id": "player"}),
        }

    def __init__(self, *args, **kwargs):
        players = kwargs.pop("players")
        super(PenaltyForm, self).__init__(*args, **kwargs)
        self.fields["player"].queryset = players
        self.fields["period"].label = "Period"
        self.fields["severity"].label = "Severity"
        self.fields["length"].label = "Length"
        self.fields["type"].label = "Type"
        self.fields["timeCommitted"].label = "Time"
        self.fields["player"].label = "Player"


PenaltyFormSet = modelformset_factory(model=Penalty, form=PenaltyForm, extra=1)


class GoalForm(ModelForm):
    class Meta:
        model = Goal
        fields = {
            "goalScorer",
            "assistPrimary",
            "assistSecondary",
            "period",
            "timeScored",
        }
        label = {
            "goalScorer": "Goal Scorer",
            "assistPrimary": "Primary Assist",
            "assistSecondary": "Secondary Assist",
            "period": "Period",
            "timeScored": "Time Scored",
        }
        widgets = {
            "goalScorer": Select(attrs={"class": "form-control", "id": "goalScorer"}),
            "assistPrimary": Select(
                attrs={"class": "form-control", "id": "assistPrimary"}
            ),
            "assistSecondary": Select(
                attrs={"class": "form-control", "id": "assistSecondary"}
            ),
            "period": Select(attrs={"class": "form-control", "id": "goalPeriod"}),
            "timeScored": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Time",
                    "id": "timeScored",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        players = kwargs.pop("players")
        super(GoalForm, self).__init__(*args, **kwargs)
        self.fields["goalScorer"].queryset = players
        # self.fields['goalScorer'].required = True
        self.fields["assistPrimary"].queryset = players
        self.fields["assistSecondary"].queryset = players
        self.fields["goalScorer"].label = "Goal Scorer"
        self.fields["assistPrimary"].label = "Primary Assist"
        self.fields["assistSecondary"].label = "Secondary Assist"
        self.fields["period"].label = "Period"
        self.fields["timeScored"].label = "Time Scored"
        self.fields["timeScored"].widget.attrs["required"] = "required"
        self.fields["period"].widget.attrs["required"] = "required"
        self.fields["goalScorer"].widget.attrs["required"] = "required"

    #
    #     self.fields['goalScorer'].widget.attrs.update({
    #         ''
    #     })


GoalFormSet = modelformset_factory(model=Goal, form=GoalForm, extra=1)


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ["homeTeam", "awayTeam", "iceSlot", "scorekeeper", "referees"]

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields["homeTeam"].label = "Home Team"
        self.fields["homeTeam"].widget = Select(
            attrs={"class": "form-control", "id": "homeTeam", "required": "required"}
        )
        self.fields["homeTeam"].queryset = Team.objects.all()
        self.fields["awayTeam"].label = "Away Team"
        self.fields["awayTeam"].widget = Select(
            attrs={"class": "form-control", "id": "awayTeam", "required": "required"}
        )
        self.fields["awayTeam"].queryset = Team.objects.all()
        self.fields["iceSlot"].label = "Ice Slot"
        self.fields["iceSlot"].widget = Select(
            attrs={"class": "form-control", "id": "iceSlot", "required": "required"}
        )
        self.fields["iceSlot"].queryset = IceSlot.objects.filter(available=True)
        self.fields["scorekeeper"].label = "Scorekeeper"
        self.fields["scorekeeper"].widget = Select(
            attrs={"class": "form-control", "id": "scorekeeper"}
        )
        self.fields["scorekeeper"].queryset = Scorekeeper.objects.all()
        self.fields["referees"].label = "Referees"
        self.fields["referees"].widget = SelectMultiple(
            attrs={
                "class": "form-control",
                "id": "referees",
            }
        )
        self.fields["referees"].queryset = Referee.objects.all()


GameFormSet = modelformset_factory(model=Game, form=GameForm, extra=1)


class IceSlotForm(ModelForm):
    class Meta:
        model = IceSlot
        fields = ["rink", "date", "time"]

    def __init__(self, *args, **kwargs):
        super(IceSlotForm, self).__init__(*args, **kwargs)
        self.fields["rink"].label = "Rink"
        self.fields["rink"].widget = Select(
            attrs={"class": "form-control", "id": "iceSlotRink", "required": "required"}
        )
        self.fields["rink"].queryset = Rink.objects.all()

        self.fields["date"].label = "Date"
        self.fields["date"].widget = DateInput(
            attrs={
                "class": "form-control",
                "type": "date",
                "id": "iceSlotDate",
                "value": date.today(),
                "required": "required",
            }
        )
        self.fields["time"].label = "Time"
        self.fields["time"].widget = TimeInput(
            attrs={
                "class": "form-control",
                "type": "time",
                "id": "iceSlotTime",
                "value": "20:30:00",
            }
        )


IceSlotFormSet = modelformset_factory(model=IceSlot, form=IceSlotForm, extra=1)


class SeasonForm(ModelForm):
    class Meta:
        model = Season
        fields = ["name", "startDate", "endDate", "numGames"]
        labels = {
            "name": "Season Name",
            "startDate": "Start Date",
            "endDate": "End Date",
            "numGames": "# of Games",
        }
        widgets = {
            "startDate": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "id": "seasonStartDate",
                    "value": date.today(),
                }
            ),
            "endDate": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                    "id": "seasonEndDate",
                    "value": date.today(),
                }
            ),
            "name": forms.TextInput(
                attrs={"class": "form-control", "id": "seasonName"}
            ),
            "numGames": forms.TextInput(
                attrs={"class": "form-control", "id": "seasonNumGames"}
            ),
        }

    # def __init__(self, *args, **kwargs):
    #     super(SeasonForm, self).__init__(*args, **kwargs)
    #
    #     for name, field in self.fields.items():
    #         field.widget.attrs.update({'class': 'form-control'})
    #
    #     self.fields['startDate'].widget.attrs.update({'type': 'date', 'id': 'seasonStartDate', 'value': date.today()})
    #     self.fields['endDate'].widget.attrs.update({'type': 'date', 'id': 'seasonStartDate', 'value': date.today()})


class DivisionForm(ModelForm):
    class Meta:
        model = Division
        fields = ["season", "name"]

    def __init__(self, *args, **kwargs):
        super(DivisionForm, self).__init__(*args, **kwargs)
        self.fields["season"].label = "Season"
        self.fields["season"].widget = Select(
            attrs={"class": "form-control", "id": "season", "required": "required"}
        )
        self.fields["season"].queryset = Season.objects.filter(seasonCompleted=False)
        self.fields["name"].label = "Name"
        self.fields["name"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Name",
                "id": "divisionName",
                "required": "required",
            }
        )


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ["division", "name"]

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields["division"].label = "Division"
        self.fields["division"].widget = Select(
            attrs={"class": "form-control", "id": "division", "required": "required"}
        )
        self.fields["division"].queryset = Division.objects.filter(
            season__seasonCompleted=False
        )
        self.fields["name"].label = "Name"
        self.fields["name"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Name",
                "id": "teamName",
                "required": "required",
            }
        )


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = [
            "team",
            "firstName",
            "lastName",
            "jerseyNumber",
            "position",
            "isCaptain",
            "isAltCaptain",
        ]

    def __init__(self, *args, **kwargs):
        super(PlayerForm, self).__init__(*args, **kwargs)
        self.fields["team"].label = "Team"
        self.fields["team"].widget = Select(
            attrs={"class": "form-control", "id": "team", "required": "required"}
        )
        self.fields["team"].queryset = Team.objects.filter(
            division__season__seasonCompleted=False
        )

        self.fields["firstName"].label = "First Name"
        self.fields["firstName"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "First Name",
                "id": "firstName",
                "required": "required",
            }
        )

        self.fields["lastName"].label = "Last Name"
        self.fields["lastName"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Name",
                "id": "Last Name",
                "required": "required",
            }
        )

        self.fields["jerseyNumber"].label = "Jersey #"
        self.fields["jerseyNumber"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Jersey #",
                "id": "jerseyNumber",
                "required": "required",
            }
        )

        self.fields["position"].label = "Position"
        self.fields["position"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Position",
                "id": "position",
            }
        )

        self.fields["isCaptain"].label = "Captain"
        self.fields["isCaptain"].widget = CheckboxInput(
            attrs={
                "class": "form-control",
                "id": "captain",
            }
        )

        self.fields["isAltCaptain"].label = "Alt Captain"
        self.fields["isAltCaptain"].widget = CheckboxInput(
            attrs={
                "class": "form-control",
                "id": "altCaptain",
            }
        )


class ScorekeeperForm(ModelForm):
    class Meta:
        model = Scorekeeper
        fields = ["name", "phoneNumber", "email"]

    def __init__(self, *args, **kwargs):
        super(ScorekeeperForm, self).__init__(*args, **kwargs)
        self.fields["name"].label = "Full Name"
        self.fields["name"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Full name",
                "id": "name",
                "required": "required",
            }
        )

        self.fields["phoneNumber"].label = "Phone Number"
        self.fields["phoneNumber"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone Number",
                "id": "phoneNumber",
                "required": "required",
            }
        )

        self.fields["email"].label = "Email"
        self.fields["email"].widget = TextInput(
            attrs={
                "class": "form-control",
                "type": "email",
                "placeholder": "email@email.com",
                "id": "email",
                "required": "required",
            }
        )


class RefereeForm(ModelForm):
    class Meta:
        model = Referee
        fields = ["name", "phoneNumber", "email"]

    def __init__(self, *args, **kwargs):
        super(RefereeForm, self).__init__(*args, **kwargs)
        self.fields["name"].label = "Full Name"
        self.fields["name"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Full name",
                "id": "name",
                "required": "required",
            }
        )

        self.fields["phoneNumber"].label = "Phone Number"
        self.fields["phoneNumber"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone Number",
                "id": "phoneNumber",
                "required": "required",
            }
        )

        self.fields["email"].label = "Email"
        self.fields["email"].widget = TextInput(
            attrs={
                "class": "form-control",
                "type": "email",
                "placeholder": "email@email.com",
                "id": "email",
                "required": "required",
            }
        )


class RinkForm(ModelForm):
    class Meta:
        model = Rink
        fields = ["name", "streetAddress", "city", "state", "zip", "phoneNumber"]

    def __init__(self, *args, **kwargs):
        super(RinkForm, self).__init__(*args, **kwargs)
        self.fields["name"].label = "Name"
        self.fields["name"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Rink Name",
                "id": "name",
                "required": "required",
            }
        )

        self.fields["streetAddress"].label = "Street Address"
        self.fields["streetAddress"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Address",
                "id": "streetAddress",
                "required": "required",
            }
        )

        self.fields["city"].label = "City"
        self.fields["city"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "City",
                "id": "city",
                "required": "required",
            }
        )

        self.fields["state"].label = "State"
        self.fields["state"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "State",
                "id": "state",
                "required": "required",
            }
        )

        self.fields["zip"].label = "Zip Code"
        self.fields["zip"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Zip Code",
                "id": "zip",
                "required": "required",
            }
        )

        self.fields["phoneNumber"].label = "Phone Number"
        self.fields["phoneNumber"].widget = TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Phone Number",
                "id": "phoneNumber",
                "required": "required",
            }
        )
