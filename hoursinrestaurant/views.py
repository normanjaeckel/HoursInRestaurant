from collections import defaultdict
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils import formats
from django.views.generic import TemplateView

from .models import Coworking, Remarks, Restaurant, WorkingDay


class Overview(LoginRequiredMixin, TemplateView):
    template_name = "overview.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        days = defaultdict(
            lambda: {
                "date_obj": None,
                "hours": [],
                "hours_total": 0,
                "coworking_total": 0,
                "work_total": 0,
                "staffs": [],
                "staff_total": 0,
                "conclusio": "",
            }
        )

        for wd in WorkingDay.objects.all():
            days[formats.date_format(wd.date)]["date_obj"] = wd.date
            days[formats.date_format(wd.date)]["hours"].append(wd)
            days[formats.date_format(wd.date)]["hours_total"] += wd.total()

        for day in days:
            date = days[day]["date_obj"]
            days[day]["coworking_total"] = Coworking.objects.filter(
                begin__lte=date, end__gte=date
            ).aggregate(Sum("hours", default=0.0))["hours__sum"]
            days[day]["work_total"] = (
                days[day]["hours_total"] + days[day]["coworking_total"]
            )
            for re in Restaurant.objects.all():
                days[day]["staffs"].extend(re.staff_at_date(days[day]["date_obj"]))
            days[day]["staff_total"] = sum(
                (staff.hours for staff in days[day]["staffs"])
            )
            diff = days[day]["work_total"] - days[day]["staff_total"]
            if diff > 0:
                days[day][
                    "conclusio"
                ] = f"Der Bedarf wird um {formats.number_format(diff,1)} Personenstunden überschritten."

        context["days"] = sorted(days.items(), key=lambda t: t[1]["date_obj"])

        remarks = [remark.text for remark in Remarks.objects.all()]
        context["remarks"] = "\n\n".join(remarks)
        return context
