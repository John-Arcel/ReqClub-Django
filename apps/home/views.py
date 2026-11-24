from datetime import datetime, timedelta
from itertools import groupby
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from .models import RunPost, RunningClub
from .forms import RunPostForm


def _get_home_context(request, form=None, open_create_modal=False):
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
    runs_qs = (
        RunPost.objects
        .select_related("club", "created_by")
        .prefetch_related("participants")
        .filter(date=selected_date)
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

    if form is None:
        form = RunPostForm(initial={"date": selected_date})

    return {
        "date_strip": date_strip,
        "selected_date": selected_date.strftime("%Y-%m-%d"),
        "grouped_runs": grouped_runs,
        "search_query": search_query,
        "run_type_filter": run_type_filter,
        "run_types": [choice[0] for choice in RunPost.RUN_TYPE_CHOICES],
        "total_runs_today": runs_qs.count(),
        "form": form,
        "open_create_modal": open_create_modal,
    }


def home_dashboard(request):
    open_modal = request.GET.get("create") == "1"
    context = _get_home_context(request, open_create_modal=open_modal)
    return render(request, "home/home.html", context)


@login_required
def toggle_join_run(request, run_id):
    if request.method == "POST":
        run_post = get_object_or_404(RunPost, id=run_id)

        # Host is auto-joined and stays in the run; only non-hosts can join/leave
        if run_post.created_by != request.user:
            if request.user in run_post.participants.all():
                run_post.participants.remove(request.user)
            elif not run_post.is_full:
                run_post.participants.add(request.user)

    return redirect(request.META.get("HTTP_REFERER", "home:home"))


@login_required
def create_run(request):
    if request.method == "POST":
        form = RunPostForm(request.POST)

        if form.is_valid():
            run_post = form.save(commit=False)

            # Set the creator as the host
            run_post.created_by = request.user

            # Use the default ReqClub community
            community_club, _ = RunningClub.objects.get_or_create(
                slug="community-runs",
                defaults={
                    "name": "ReqClub Community",
                    "city": "Cebu City",
                    "avatar_Bg": "bg-amber-500",
                },
            )

            run_post.club = community_club
            run_post.save()

            # Auto-join the host to the run
            run_post.participants.add(request.user)

            return redirect(
                f"{reverse('home:home')}?date={run_post.date.strftime('%Y-%m-%d')}"
            )

        context = _get_home_context(request, form=form, open_create_modal=True)
        return render(request, "home/home.html", context)

    return redirect(f"{reverse('home:home')}?create=1")