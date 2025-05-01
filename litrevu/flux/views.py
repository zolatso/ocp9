from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.shortcuts import render, redirect
from .models import Ticket, Review
from itertools import chain
from .forms import TicketReviewForm

@login_required
def ticket_review_create(request):
    if request.method == "POST":
        form = TicketReviewForm(request.POST, request.FILES)
        if form.is_valid():
            Ticket.objects.create(
                title = form.cleaned_data['ticket_title'],
                description = form.cleaned_data['ticket_description'],
                user = request.user,
                image = form.cleaned_data['ticket_image']
            )
            Review.objects.create(
                ticket = Ticket.objects.latest(),
                rating = form.cleaned_data['review_rating'],
                headline = form.cleaned_data['review_headline'],
                body = form.cleaned_data['review_body'],
                user = request.user
            )
            return redirect("/home/")
    else:
        form = TicketReviewForm()
        return render(request, "flux/ticket_review_form.html", {"form": form})

@login_required
def home(request):
    tickets = Ticket.objects.filter(user__followed_by__user=request.user)
    reviews = Review.objects.filter(user__followed_by__user=request.user)
    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True)
    context = {"posts" : posts}
    return render(request, 'flux/home.html', context)

# class HomeView(LoginRequiredMixin, ListView):
#     model = Ticket
#     ordering = '-time_created'
#     template_name = 'flux/home.html'
#     context_object_name = "tickets"

@login_required
def my_posts(request):
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    posts = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True)
    context = {"posts" : posts}
    return render(request, 'flux/my_posts.html', context)

class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = '/home/'

class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ['title', 'description', 'image']
    success_url = '/home/'

    def form_valid(self, form):
        # Set the user to the currently logged in user
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'headline', 'body']
    success_url = '/home/'
    
    def form_valid(self, form):
        # Set the user to the currently logged in user
        form.instance.user = self.request.user
        # Link it to the ticket provided in the URL
        ticket_id = self.kwargs['id']
        form.instance.ticket = Ticket.objects.get(id=ticket_id)
        return super().form_valid(form)