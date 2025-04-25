from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Ticket, Review

@login_required
def home(request):
    return render(request, 'flux/home.html')
