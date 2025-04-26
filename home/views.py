from django.shortcuts import render, redirect, get_object_or_404

from .forms import PlanForm
from .models import Plan, Joined, Comment
from django.contrib.auth.decorators import login_required
'''i made a new version of this, i think this can be deleted
def index(request):
    template_data = {}
    template_data['title'] = 'Movies Store'
    return render(request, 'home/index.html', {'template_data': template_data})
'''

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
        plans = Plan.objects.filter(name__icontains=search_term)
    else:
        plans = Plan.objects.all()

    template_data = {}
    template_data['name'] = 'Plans'
    template_data['plans'] = plans
    # TODO need to implement html stuff for below to work! vvv
    return render(request, 'home/index.html', {'template_data': template_data})
"""
Showing plan
"""
def show(request, id):
    plan = Plan.objects.get(id=id)
    comments = Comment.objects.filter(plan=plan)

    template_data = {}
    template_data['name'] = plan.name
    template_data['plan'] = plan
    template_data['comments'] = comments
    # TODO need to implement html stuff for below to work! vvv
    return render(request, 'home/show.html', {'template_data': template_data})

@login_required
def join_plan(request, id):
    plan = get_object_or_404(Plan, id=id)
    if not Joined.objects.filter(plan=plan, user=request.user).exists():
        Joined.objects.create(plan=plan, user=request.user)
    return redirect('plan.show', id=id)

@login_required
def add_comment(request, id):
    if request.method == 'POST':
        text = request.POST.get('text')
        plan = get_object_or_404(Plan, id=id)
        Comment.objects.create(user=request.user, plan=plan, text=text)
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
    plans = (
        Plan.objects
        .filter(user=request.user)
        .order_by("-date")  # newest → oldest
    )
    return render(request, "accounts/plans.html", {"plans": plans})


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
            form.save()
            return redirect("accounts.plans")
    else:
        form = PlanForm(instance=plan)
    return render(request, "accounts/add_plan.html",
                  {"form": form, "editing": True})

@login_required
def delete_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk, user=request.user)
    if request.method == "POST":
        plan.delete()
    return redirect("accounts.plans")

