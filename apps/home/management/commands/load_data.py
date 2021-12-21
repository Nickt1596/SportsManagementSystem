from django.core.management.base import BaseCommand, CommandError
from apps.home.models import *


class Command(BaseCommand):
    help = 'Load Divisions'

    def handle(self, *args, **options):
        loadDivisions()
        loadTeams()
        return

