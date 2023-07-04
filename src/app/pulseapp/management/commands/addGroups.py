from django.core.management.base import BaseCommand
from pulseapp.views import addGroups,addSiteData,adduwtp,addSampleData,addMeasureData,addTrendsData,addVariantsData

class Command(BaseCommand):
    help="Add groups to database"
    def handle(self, *args, **kwargs):
        # addGroups()
        # addSiteData()
        # adduwtp()
        addSampleData()
        addMeasureData()
        addTrendsData()
        addVariantsData()
