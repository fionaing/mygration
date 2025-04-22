from django.shortcuts import render, redirect, get_object_or_404
from .models import Plan, Joined, Comment
from django.contrib.auth.decorators import login_required

def index(request):
    template_data = {}
    template_data['title'] = 'Movies Store'
    return render(request, 'home/index.html', {'template_data': template_data})

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
    return render(request, 'plans/show.html', {'template_data': template_data})