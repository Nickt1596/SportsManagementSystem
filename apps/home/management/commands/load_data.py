from django.core.management.base import BaseCommand, CommandError
from apps.home.models import *


class Command(BaseCommand):
    help = 'Populate Databases'

    def handle(self, *args, **options):
        populateDatabases()
        return

