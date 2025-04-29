from django.urls import path

from .views import TicketCreateView, ReviewCreateView, home, ticket_review_create


urlpatterns = [
    path('', home, name='home'),
    path('ticket/create/', TicketCreateView.as_view(), name='ticket-create'),
    path('review/create/<int:id>/', ReviewCreateView.as_view(), name='review-create'),
    path('ticket-review/create/', ticket_review_create, name='ticket-review-create')
]