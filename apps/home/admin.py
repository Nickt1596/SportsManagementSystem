# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Season)
admin.site.register(Division)
admin.site.register(Team)
admin.site.register(TeamStats)
admin.site.register(Player)
admin.site.register(PlayerStats)
admin.site.register(Rink)
admin.site.register(Game)
admin.site.register(Referee)
admin.site.register(Scorekeeper)
admin.site.register(IceSlot)
admin.site.register(Goal)
admin.site.register(Penalty)
admin.site.register(GameResult)
