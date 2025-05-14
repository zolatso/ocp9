from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Value, CharField, Exists, OuterRef, Q
from django.views.generic import CreateView, DeleteView, UpdateView
from django.shortcuts import render, redirect
from .models import Ticket, Review, UserFollows
from authenticate.models import User
from itertools import chain
from .forms import TicketReviewForm, FollowUserForm, ReviewForm


@login_required
def home(request):
    followed_users = request.user.following.values_list("followed_user", flat=True)
    tickets = Ticket.objects.filter(
        Q(user=request.user) | Q(user__in=followed_users)
    ).annotate(
        content_type=Value("TICKET", CharField()),
        has_review=Exists(Review.objects.filter(ticket=OuterRef("pk"))),
    )
    reviews = (
        Review.objects.filter(Q(user=request.user) | Q(user__in=followed_users))
        .select_related("ticket")
        .annotate(content_type=Value("REVIEW", CharField()))
    )
    posts = sorted(
        chain(tickets, reviews), key=lambda post: post.time_created, reverse=True
    )
    context = {"posts": posts}
    return render(request, "flux/home.html", context)


@login_required
def my_posts(request):
    tickets = Ticket.objects.filter(user=request.user).annotate(
        content_type=Value("TICKET", CharField())
    )
    reviews = (
        Review.objects.filter(user=request.user)
        .select_related("ticket")
        .annotate(content_type=Value("REVIEW", CharField()))
    )
    posts = sorted(
        chain(tickets, reviews), key=lambda post: post.time_created, reverse=True
    )
    context = {"posts": posts}
    return render(request, "flux/my_posts.html", context)


@login_required
def abonnements(request):
    following = UserFollows.objects.filter(user=request.user).exclude(
        followed_user=request.user
    )
    followed_by = UserFollows.objects.filter(followed_user=request.user).exclude(
        user=request.user
    )
    form = FollowUserForm()
    context = {"form": form, "following": following, "followers": followed_by}
    return render(request, "flux/abonnements.html", context)


@login_required
def remove_follower(request, id):
    follower = UserFollows.objects.filter(followed_user=request.user).filter(user=id)
    follower.delete()
    return redirect("/home/abonnements/")


@login_required
def unfollow(request, id):
    user_to_unfollow = UserFollows.objects.filter(followed_user=id).filter(
        user=request.user
    )
    user_to_unfollow.delete()
    return redirect("/home/abonnements/")


@login_required
def follow_user(request):
    if request.method == "POST":
        form = FollowUserForm(request.POST)
        if form.is_valid():
            user = request.user
            user_to_follow = form.cleaned_data["user_to_follow"]
            if not User.objects.filter(username=user_to_follow).exists():
                messages.error(request, "Cet utilisateur n'existe pas.")
                return redirect("abonnements")
            else:
                user_id = User.objects.get(username=user_to_follow)
                UserFollows.objects.create(user=user, followed_user=user_id)
                return redirect("abonnements")


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    fields = ["title", "description", "image"]
    success_url = "/home/"

    def form_valid(self, form):
        # Set the user to the currently logged in user
        form.instance.user = self.request.user
        return super().form_valid(form)


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = "/home/my_posts/"


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    fields = ["title", "description", "image"]
    success_url = "/home/my_posts/"


class ReviewCreateView(LoginRequiredMixin, CreateView, ReviewForm):
    model = Review
    success_url = "/home/"
    form_class = ReviewForm

    def form_valid(self, form):
        # Set the user to the currently logged in user
        form.instance.user = self.request.user
        # Link it to the ticket provided in the URL
        ticket_id = self.kwargs["id"]
        form.instance.ticket = Ticket.objects.get(id=ticket_id)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket_id = self.kwargs["id"]
        ticket = Ticket.objects.get(id=ticket_id)
        context["ticket"] = ticket  # Add any info you want from the ticket
        return context


class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = "/home/my_posts/"


class ReviewUpdateView(LoginRequiredMixin, UpdateView, ReviewForm):
    model = Review
    form_class = ReviewForm
    success_url = "/home/my_posts/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = self.object
        context["ticket"] = review.ticket  # Add any info you want from the ticket
        return context


@login_required
def ticket_review_create(request):
    if request.method == "POST":
        form = TicketReviewForm(request.POST, request.FILES)
        if form.is_valid():
            Ticket.objects.create(
                title=form.cleaned_data["ticket_title"],
                description=form.cleaned_data["ticket_description"],
                user=request.user,
                image=form.cleaned_data["ticket_image"],
            )
            Review.objects.create(
                ticket=Ticket.objects.latest(),
                rating=form.cleaned_data["review_rating"],
                headline=form.cleaned_data["review_headline"],
                body=form.cleaned_data["review_body"],
                user=request.user,
            )
            return redirect("/home/")
    else:
        form = TicketReviewForm()
        return render(request, "flux/ticket_review_form.html", {"form": form})


# class HomeView(LoginRequiredMixin, ListView):
#     model = Ticket
#     ordering = '-time_created'
#     template_name = 'flux/home.html'
#     context_object_name = "tickets"
