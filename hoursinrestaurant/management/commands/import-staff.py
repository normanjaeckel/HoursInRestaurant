import csv
import datetime

from django.core.management.base import BaseCommand
from hoursinrestaurant.models import Restaurant, Staff

WEEKDAY_MAP = {
    "Montag": "1",
    "Dienstag": "2",
    "Mittwoch": "3",
    "Donnerstag": "4",
    "Freitag": "5",
    "Sonnabend": "6",
    "Sonntag": "7",
}

class Command(BaseCommand):
    help = "Mass import of staff from CSV"

    def add_arguments(self, parser):
        parser.add_argument("filename", type=open)

    def handle(self, *args, **options):
        file = csv.DictReader(options["filename"])
        for row in file:
            re = Restaurant.objects.get(name=row["Restaurant"])
            we = WEEKDAY_MAP[row["Wochentag"]]
            begin = datetime.datetime.strptime(row["Gültig von"], "%Y-%m-%d").date()
            end = datetime.datetime.strptime(row["Gültig bis"] or row["Gültig von"], "%Y-%m-%d").date()  # TODO
            Staff.objects.create(restaurant=re, weekday=we, begin=begin, end=end, opening=row["Öffnungszeiten"], hours=row["Personenstunden"] or 0)  # TODO

