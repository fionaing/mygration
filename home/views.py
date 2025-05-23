from django.shortcuts import render, redirect, get_object_or_404

from mygration.helper_functions.fetch_weather_data import fetch_weather_data
from .forms import PlanForm
from .models import Plan, Joined, Comment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from mygration.helper_functions.fetch_weather_data import fetch_weather_data

def about(request):
    template_data = {}
    template_data['title'] = 'About'
    return render(request, 'home/about.html', {'template_data': template_data})


"""
Searching for plans
"""
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        plans = Plan.objects.filter(name__icontains=search_term, public=True)
    else:
        plans = Plan.objects.filter(public=True)

    template_data = {}
    template_data['name'] = 'Plans'
    template_data['plans'] = plans
    # TODO need to implement html stuff for below to work! vvv
    return render(request, 'home/index.html', {'template_data': template_data})
"""
Showing plan
"""
@login_required
def show(request, id):
    plan = Plan.objects.get(id=id)
    comments = Comment.objects.filter(plan=plan)
    joined = Joined.objects.filter(plan=plan, user=request.user).exists()

    template_data = {}
    template_data['name'] = plan.name
    template_data['plan'] = plan
    template_data['comments'] = comments
    template_data['joined'] = joined
    template_data['weather_data'] = fetch_weather_data(plan)
    print(template_data['weather_data'])
    # TODO need to implement html stuff for below to work! vvv
    return render(request, 'home/show.html', {'template_data': template_data})

@login_required
def join_plan(request, id):
    plan = get_object_or_404(Plan, id=id)
    if not Joined.objects.filter(plan=plan, user=request.user).exists():
        Joined.objects.create(plan=plan, user=request.user)
        plan.joined = plan.joined + 1
        plan.save()
    return redirect('plan.show', id=id)

@login_required
def add_comment(request, id):
    if request.method == 'POST':
        text = request.POST.get('text')
        plan = get_object_or_404(Plan, id=id)
        Comment.objects.create(user=request.user, plan=plan, comment=text)
    return redirect('plan.show', id=id)

@login_required
def dashboard(request):
    user = request.user
    created_plans = Plan.objects.filter(user=user)
    joined_plans = Plan.objects.filter(joined__user=user)

    return render(request, 'home/dashboard.html', {
        'created_plans': created_plans,
        'joined_plans': joined_plans,
    })




@login_required
def user_plans(request):
    created_plans = Plan.objects.filter(user=request.user).order_by("-date")
    joined_plans = Plan.objects.filter(join_records__user=request.user).exclude(user=request.user).order_by("-date")

    return render(request, "accounts/plans.html", {
        "created_plans": created_plans,
        "joined_plans": joined_plans
    })


@login_required
def add_plan(request):
    if request.method == "POST":
        form = PlanForm(request.POST, request.FILES)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user        # link the logged‑in user
            plan.save()
            return redirect("accounts.plans")  # after save go to /plans/
    else:
        form = PlanForm()

    return render(request, "accounts/add_plan.html", {"form": form})

@login_required
def edit_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk, user=request.user)
    if request.method == "POST":
        form = PlanForm(request.POST, request.FILES, instance=plan)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user        # link the logged‑in user
            form.save()
            return redirect("accounts.plans")
    else:
        form = PlanForm(instance=plan)
    return render(request, "accounts/add_plan.html",
                  {"form": form, "editing": True})

@login_required
@require_POST
def leave_plan(request, id):
    plan = get_object_or_404(Plan, id=id)
    Joined.objects.filter(plan=plan, user=request.user).delete()
    plan.joined = plan.joined - 1
    plan.save()
    return redirect("accounts.plans")

@login_required
@require_POST
def delete_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk, user=request.user)
    plan.delete()
    return redirect('accounts.plans')

@login_required
@require_POST
def add_comment(request, id):
    plan = get_object_or_404(Plan, id=id)
    text = request.POST.get('text')
    if text:
        Comment.objects.create(user=request.user, plan=plan, comment=text)
        messages.success(request, "Your comment was posted successfully!")
    else:
        messages.error(request, "You must write something to post a comment.")
    return redirect('plan.show', id=id)
