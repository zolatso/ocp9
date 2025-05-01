from django.urls import path

from .views import TicketCreateView, TicketDeleteView, ReviewCreateView, home, my_posts


urlpatterns = [
    path('', home, name='home'),
    path('ticket/create/', TicketCreateView.as_view(), name='ticket-create'),
    path('review/create/<int:id>/', ReviewCreateView.as_view(), name='review-create'),
    path('my_posts/', my_posts, name='my_posts'),
    path('<pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
]