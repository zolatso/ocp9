from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.shortcuts import render
from .models import Ticket, Review

@login_required
def home(request):
    tickets = Ticket.objects.order_by("time_created")
    context = {"tickets" : tickets}
    return render(request, 'flux/home.html', context)

class HomeView(LoginRequiredMixin, ListView):
    model = Ticket
    ordering = 'time_created'
    template_name = 'flux/home.html'
    context_object_name = "tickets"

class TicketCreateView(CreateView):
    model = Ticket
    fields = '__all__'