import datetime
from collections import OrderedDict

from django.contrib import admin
from django.db import models
from django.utils import formats


class Employee(models.Model):
    last_name = models.CharField(max_length=255, verbose_name="Nachname")
    first_name = models.CharField(max_length=255, verbose_name="Vorname")

    class Meta:
        verbose_name = "Arbeitnehmer/in"
        verbose_name_plural = "Arbeitnehmer/innen"

    def __str__(self):
        return " ".join([self.first_name, self.last_name])


class Volume(models.Model):
    name = models.CharField(max_length=255, verbose_name="Bezeichnung")

    class Meta:
        verbose_name = "Aktenband"
        verbose_name_plural = "Aktenbände"

    def __str__(self):
        return self.name


class Sheet(models.Model):
    volume = models.ForeignKey(
        Volume, on_delete=models.PROTECT, verbose_name="Aktenband"
    )
    page = models.CharField(max_length=255, verbose_name="Seite")
    employee = models.ForeignKey(
        Employee, on_delete=models.PROTECT, verbose_name="Arbeitnehmer/in"
    )

    class Meta:
        verbose_name = "Stundenzettel"
        verbose_name_plural = "Stundenzettel"

    def __str__(self):
        return f"{self.source()} · {self.employee}"

    @admin.display(description="Fundstelle")
    def source(self):
        return f"{self.volume} Seite {self.page}"

    @admin.display(description="Monate")
    def months(self):
        months = []
        for wd in self.working_days.all():
            months.append(formats.date_format(wd.date, "F Y"))
        return ", ".join(OrderedDict().fromkeys(months))


class WorkingDay(models.Model):
    sheet = models.ForeignKey(
        Sheet,
        on_delete=models.PROTECT,
        verbose_name="Stundenzettel",
        related_name="working_days",
    )
    date = models.DateField(verbose_name="Datum")
    begin = models.TimeField(verbose_name="Beginn der Arbeitszeit")
    end = models.TimeField(verbose_name="Ende der Arbeitszeit")
    break_time = models.PositiveIntegerField(verbose_name="Pause (in Minuten)")

    class Meta:
        verbose_name = "Arbeitstag"
        verbose_name_plural = "Arbeitstage"

    def __str__(self):
        return f"{formats.date_format(self.date)} · {self.sheet.employee}"

    @admin.display(description="Arbeitnehmer/in")
    def employee(self):
        return self.sheet.employee

    @admin.display(description="Arbeitszeit")
    def time(self):
        return self.begin.strftime("%H:%M") + " – " + self.end.strftime("%H:%M")

    @admin.display(description="Pause")
    def break_time_display(self):
        return f"{self.break_time} Min."

    @admin.display(description="Stunden")
    def total(self):
        end = datetime.timedelta(hours=self.end.hour, minutes=self.end.minute)
        begin = datetime.timedelta(hours=self.begin.hour, minutes=self.begin.minute)
        break_time = datetime.timedelta(minutes=self.break_time)
        delta = end - begin - break_time
        return round(delta.total_seconds() / 3600, 2)


class Restaurant(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return self.name


class Staff(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.PROTECT, verbose_name="Restaurant"
    )
    begin = models.TimeField(verbose_name="Beginn der Arbeitszeit")
    end = models.TimeField(verbose_name="Ende der Arbeitszeit")
    # weekdays
    # date_from
    # date_until
    # additional_days
    # excluded_days

    class Meta:
        verbose_name = "Mitarbeiter"
        verbose_name_plural = "Mitarbeiter"

    def __str__(self):
        return f"{self.restaurant} {self.begin.strftime("%H:%M")} – {self.end.strftime("%H:%M")}"
