from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from flux.models import Review


class TicketReviewForm(forms.Form):
    RATING_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    ]
    ticket_title = forms.CharField(max_length=128)
    ticket_description = forms.CharField(max_length=2048)
    ticket_image = forms.ImageField()
    review_rating = forms.ChoiceField(
        choices=RATING_CHOICES, widget=forms.RadioSelect(), label="Rating"
    )
    review_headline = forms.CharField(max_length=128)
    review_body = forms.CharField(max_length=8192)


class FollowUserForm(forms.Form):
    user_to_follow = forms.CharField(max_length=150)


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    ]
    rating = forms.ChoiceField(
        choices=RATING_CHOICES, widget=forms.RadioSelect(), label="Rating"
    )

    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]
