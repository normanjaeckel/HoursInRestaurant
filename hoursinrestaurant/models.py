import datetime

from django.db import models
from django.contrib import admin

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
    volume = models.ForeignKey(Volume, on_delete=models.PROTECT)
    page = models.CharField(max_length=255, verbose_name="Seite")
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    date = models.DateField(verbose_name="Datum")
    begin = models.TimeField(verbose_name="Beginn der Arbeitszeit")
    end = models.TimeField(verbose_name="Ende der Arbeitszeit")
    break_time = models.PositiveIntegerField(verbose_name="Pause (in Minuten)")

    class Meta:
        verbose_name = "Stundenzettel"
        verbose_name_plural = "Stundenzettel"

    def __str__(self):
        return self.source()

    @admin.display(description="Fundstelle")
    def source(self):
        return f"{self.volume} Seite {self.page}"

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

