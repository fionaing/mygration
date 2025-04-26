from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from.models import Warning
from .forms import UpdateProfileForm

from home.models import Plan


# Create your views here
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    elif request.method == 'POST':
        # use custom forms and error display when trying to sign up
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            # Successfully creates user
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        # authenticate user
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user is None:
            # authentication fails
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            # successful authentication
            auth_login(request, user)
            return redirect('home.index')

def reset_password(request):
    template_data = {}
    template_data['title'] = 'Reset Password'
    if request.method == 'GET':
        return render(request, 'accounts/reset_password.html', {'template_data': template_data})
    elif request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username).exists() and request.POST['password'] == request.POST['password2']:
            user = User.objects.get(username=username)
            user.set_password(request.POST['password'])
            user.save()
            return redirect('accounts.login')
        elif request.POST['password'] == request.POST['password2']:
            template_data['error'] = "The username doesn't exist."
            return render(request, 'accounts/reset_password.html', {'template_data': template_data})
        else:
            template_data['error'] = "The passwords don't match."
            return render(request, 'accounts/reset_password.html', {'template_data': template_data})


@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

@login_required
def plans(request):
    template_data = {}
    template_data['title'] = 'Plans'
    template_data['plans'] = request.user.plan_set.all()
    return render(request, 'accounts/plans.html',
        {'template_data': template_data})

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='accounts.profile')
    else:
        profile_form = UpdateProfileForm(instance=request.user.profile)

    warning_data = {}
    warning_data['warnings'] = Warning.objects.filter(user=request.user)
    return render(request, 'accounts/profile.html', {'profile_form': profile_form, 'warning_data': warning_data})



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

