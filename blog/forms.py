from django import forms
from .models import Ticket, Review, UserFollows
# from django.contrib.auth.models import User

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']

class FollowUserForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']

class UserSearchForm(forms.Form):
    username = forms.CharField(max_length=150, required=False, label='Search for users')