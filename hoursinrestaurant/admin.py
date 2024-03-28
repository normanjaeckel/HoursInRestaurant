# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/

from django.contrib import admin

from .models import Employee, Sheet, Volume


class SheetAdmin(admin.ModelAdmin):
    list_display = [
        "source",
        "employee",
        "date",
        "time",
        "break_time_display",
        "total",
    ]


class AdminSite(admin.AdminSite):
    site_header = "Auswertung der Ermittlungsakten"
    site_title = "Auswertung der Ermittlungsakten"
    index_title = "Übersicht"


admin_site = AdminSite()

admin_site.register(Employee)
admin_site.register(Volume)
admin_site.register(Sheet, SheetAdmin)
