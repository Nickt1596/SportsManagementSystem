from django.core.management.base import BaseCommand, CommandError
from apps.home.models import *


class Command(BaseCommand):
    help = 'Load Refs and Scorekeepers'

    def handle(self, *args, **options):
        generateReferees()
        generateScorekeepers()
        return
