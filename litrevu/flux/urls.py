from django.urls import path

from .views import TicketCreateView, TicketDeleteView, TicketUpdateView
from .views import (
    ReviewCreateView,
    ReviewDeleteView,
    ReviewUpdateView,
    home,
    my_posts,
    ticket_review_create,
)
from .views import abonnements, remove_follower, unfollow, follow_user


urlpatterns = [
    path("", home, name="home"),
    path("my_posts/", my_posts, name="my-posts"),
    path("ticket/create/", TicketCreateView.as_view(), name="ticket-create"),
    path("ticket/delete/<pk>", TicketDeleteView.as_view(), name="ticket-delete"),
    path("ticket/update/<pk>", TicketUpdateView.as_view(), name="ticket-update"),
    path("review/create/<int:id>/", ReviewCreateView.as_view(), name="review-create"),
    path("review/delete/<pk>", ReviewDeleteView.as_view(), name="review-delete"),
    path("review/update/<pk>", ReviewUpdateView.as_view(), name="review-update"),
    path("ticket-review/create/", ticket_review_create, name="ticket-review-create"),
    path("abonnements/", abonnements, name="abonnements"),
    path(
        "abonnements/remove_follower/<int:id>", remove_follower, name="remove-follower"
    ),
    path("abonnements/unfollow/<int:id>", unfollow, name="unfollow"),
    path("abonnements/follow_user", follow_user, name="follow-user"),
]
