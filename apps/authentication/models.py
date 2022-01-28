# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    class Types(models.TextChoices):
        COMMISSIONER = "COMMISSIONER", "Commissioner"
        REFEREE = "REFEREE", "Referee"
        SCOREKEEPER = "SCOREKEEPER", "Scorekeeper"
        CAPTAIN = "CAPTAIN", "Captain"
        PLAYER = "PLAYER", "Player"

    base_type = Types.PLAYER

    type = models.CharField(max_length=50, choices=Types.choices, default=Types.PLAYER)

    # def save(self, *args, **kwargs):
    #     # If a new user, set the user's type based off the
    #     # base_type property
    #     if not self.pk:
    #         self.type = self.base_type
    #     return super().save(*args, **kwargs)


