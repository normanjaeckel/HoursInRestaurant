from collections import defaultdict
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import formats
from django.views.generic import TemplateView

from .models import Restaurant, WorkingDay


class Overview(LoginRequiredMixin, TemplateView):
    template_name = "overview.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        days = defaultdict(lambda: {"date_obj": None, "hours": [], "staffs": []})

        for wd in WorkingDay.objects.all():
            days[formats.date_format(wd.date)]["date_obj"] = wd.date
            days[formats.date_format(wd.date)]["hours"].append(wd)

        for day in days:
            for re in Restaurant.objects.all():
                days[day]["staffs"].extend(re.staff_at_date(days[day]["date_obj"]))

        context["days"] = days.items()
        return context
