from datetime import datetime, timedelta
from itertools import groupby
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from .models import RunPost, RunningClub


def home_dashboard(request):
    today = timezone.localdate()

    # 1. Selected date from query param (?date=YYYY-MM-DD)
    date_str = request.GET.get("date")
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            selected_date = today
    else:
        selected_date = today

    # 2. Build 7-day strip for the horizontal date picker
    date_strip = []
    for i in range(7):
        day = today + timedelta(days=i)
        date_strip.append({
            "full_date": day.strftime("%Y-%m-%d"),
            "day_name": day.strftime("%a").upper(),
            "day_number": day.strftime("%d"),
            "is_selected": day == selected_date,
        })

    # 3. Filter Run Posts
    runs_qs = RunPost.objects.select_related("club").prefetch_related("participants").filter(
        date=selected_date
    )

    search_query = request.GET.get("q", "").strip()
    if search_query:
        runs_qs = runs_qs.filter(
            Q(title__icontains=search_query) |
            Q(club__name__icontains=search_query) |
            Q(venue_name__icontains=search_query) |
            Q(target_pace__icontains=search_query)
        )

    run_type_filter = request.GET.get("type", "").strip()
    if run_type_filter:
        runs_qs = runs_qs.filter(run_type__iexact=run_type_filter)

    runs_qs = runs_qs.order_by("start_time")

    # 4. Group runs chronologically by start_time
    grouped_runs = []
    for start_time, items in groupby(runs_qs, key=lambda x: x.start_time):
        posts_list = list(items)
        grouped_runs.append({
            # Use %I:%M %p for cross-platform compatibility on Windows & Linux
            "time_label": start_time.strftime("%I:%M %p").lstrip("0"),
            "count": len(posts_list),
            "posts": posts_list,
        })

    context = {
        "date_strip": date_strip,
        "selected_date": selected_date.strftime("%Y-%m-%d"),
        "grouped_runs": grouped_runs,
        "search_query": search_query,
        "run_type_filter": run_type_filter,
        "run_types": [choice[0] for choice in RunPost.RUN_TYPE_CHOICES],
        "total_runs_today": runs_qs.count(),
    }
    # Points to templates/home/dashboard.html
    return render(request, "home/home.html", context)


@login_required
def toggle_join_run(request, run_id):
    if request.method == "POST":
        run_post = get_object_or_404(RunPost, id=run_id)
        if request.user in run_post.participants.all():
            run_post.participants.remove(request.user)
        elif not run_post.is_full:
            run_post.participants.add(request.user)
    return redirect(request.META.get("HTTP_REFERER", "reqclub_dashboard"))