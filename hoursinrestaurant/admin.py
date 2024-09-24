# https://docs.djangoproject.com/en/5.0/ref/contrib/admin/

from django.contrib import admin

from .models import (
    Coworking,
    Employee,
    Remarks,
    Restaurant,
    Sheet,
    Staff,
    Volume,
    WorkingDay,
)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "sheet_list",
    ]


class SheetAdmin(admin.ModelAdmin):
    list_display = [
        "source",
        "employee",
        "hours",
        "months",
    ]


class WorkingDayAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "employee",
        "time",
        "break_time_display",
        "total",
        "sheet",
    ]


class AdminSite(admin.AdminSite):
    site_header = "Auswertung der Ermittlungsakten"
    site_title = "Auswertung der Ermittlungsakten"
    index_title = "Übersicht"


admin_site = AdminSite()

admin_site.register(Coworking)
admin_site.register(Employee, EmployeeAdmin)
admin_site.register(Volume)
admin_site.register(Sheet, SheetAdmin)
admin_site.register(WorkingDay, WorkingDayAdmin)
admin_site.register(Remarks)
admin_site.register(Restaurant)
admin_site.register(Staff)
