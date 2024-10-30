from django import forms
from .models import Review, UserFollows

class ReviewForm(forms.ModelForm):
    """
    Formulaire pour créer ou éditer une critique.
    """
    RATING_CHOICES = [(i, str(i)) for i in range(6)]  # Choix de 0 à 5

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        label='Évaluation'
    )

    class Meta:
        model = Review
        fields = ['rating', 'headline', 'body']


class FollowUserForm(forms.ModelForm):
    """
    Formulaire pour suivre un utilisateur.
    """
    class Meta:
        model = UserFollows
        fields = ['followed_user']


class UserSearchForm(forms.Form):
    """
    Formulaire pour rechercher des utilisateurs.
    """
    username = forms.CharField(max_length=150, required=False, label='Rechercher des utilisateurs')