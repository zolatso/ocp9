from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Ticket, Review

@login_required
def home(request):
    tickets = Ticket.objects.order_by("time_created")
    context = {"tickets" : tickets}
    return render(request, 'flux/home.html', context)


