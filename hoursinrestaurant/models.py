import datetime
from collections import OrderedDict, defaultdict

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

    @admin.display(description="Stundenzettel")
    def sheet_list(self):
        all_sheets = defaultdict(list)
        for sheet in self.sheets.all():
            all_sheets[sheet.volume].append(sheet.page)
        result = []
        for k, v in all_sheets.items():
            result.append(f"{k} {', '.join(v)}")
        return "; ".join(result)


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
        Employee,
        on_delete=models.PROTECT,
        verbose_name="Arbeitnehmer/in",
        related_name="sheets",
    )

    class Meta:
        verbose_name = "Stundenzettel"
        verbose_name_plural = "Stundenzettel"

    def __str__(self):
        return f"{self.source()} · {self.employee}"

    @admin.display(description="Fundstelle")
    def source(self):
        return f"{self.volume} {self.page}"

    @admin.display(description="Stunden")
    def hours(self):
        total = 0
        for wd in self.working_days.all():
            total += wd.total()
        return total

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


class Coworking(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    begin = models.DateField(verbose_name="Gültig von")
    end = models.DateField(verbose_name="Gültig bis")
    hours = models.FloatField(verbose_name="Personenstunden pro Tag")

    class Meta:
        verbose_name = "Mitarbeit durch Inhaber und Angehörige"
        verbose_name_plural = "Mitarbeit durch Inhaber und Angehörige"

    def __str__(self):
        return f"{self.name} · {formats.date_format(self.begin)} – {formats.date_format(self.end)} · {self.hours} Personenstunden pro Tag"


class Restaurant(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")

    class Meta:
        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"

    def __str__(self):
        return self.name

    def staff_at_date(self, date):
        weekday = str(date.weekday()+1)
        return list(self.staffs.filter(begin__lte=date, end__gte=date, weekday=weekday))


class Staff(models.Model):
    MONDAY = "1"
    TUESDAY = "2"
    WEDNESDAY = "3"
    THURSDAY = "4"
    FRIDAY = "5"
    SATURDAY = "6"
    SUNDAY = "7"
    WEEKDAY_CHOICES = {
        MONDAY: "Montag",
        TUESDAY: "Dienstag",
        WEDNESDAY: "Mittwoch",
        THURSDAY: "Donnerstag",
        FRIDAY: "Freitag",
        SATURDAY: "Sonnabend",
        SUNDAY: "Sonntag",
    }

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.PROTECT,
        verbose_name="Restaurant",
        related_name="staffs",
    )
    weekday = models.CharField(max_length=1, verbose_name="Wochentag", choices=WEEKDAY_CHOICES)
    begin = models.DateField(verbose_name="Gültig von")
    end = models.DateField(verbose_name="Gültig bis")
    opening = models.CharField(max_length=255, verbose_name="Öffnungszeiten", blank=True)
    hours = models.FloatField(verbose_name="Personenstunden")

    class Meta:
        verbose_name = "Mitarbeiterbedarf"
        verbose_name_plural = "Mitarbeiterbedarf"

    def __str__(self):
        return f"{self.restaurant} · {self.get_weekday_display()} ({formats.date_format(self.begin)} – {formats.date_format(self.end)}) {self.opening} · {self.hours} Personenstunden"

class Remarks(models.Model):
    text = models.TextField(verbose_name="Text", help_text="Leerzeilen erzeugen Absätze")

    class Meta:
        verbose_name = "Vorbemerkung"
        verbose_name_plural = "Vorbemerkungen"

    def __str__(self):
        return f"Vorbemerkung {self.pk}"
