from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import SetPasswordForm
from .forms import CustomUserCreationForm, CustomErrorList
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
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
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})