from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class TicketReviewForm(forms.Form):
    ticket_title = forms.CharField(max_length=128)
    ticket_description = forms.CharField(max_length=2048)
    ticket_image = forms.ImageField()
    review_rating = forms.IntegerField()
    review_headline = forms.CharField(max_length=128)
    review_body = forms.CharField(max_length=8192)

class FollowUserForm(forms.Form):
    user_to_follow = forms.CharField(max_length=150)

