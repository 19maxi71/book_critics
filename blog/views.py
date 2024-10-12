from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Value, CharField
from .models import Review, Ticket, UserFollows
from itertools import chain
from django.contrib.auth.forms import UserCreationForm
from .forms import TicketForm, ReviewForm, FollowUserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('blog:feed')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def feed(request):
    following_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    reviews = Review.objects.filter(user__in=following_users) | Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = Ticket.objects.filter(user__in=following_users) | Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
    return render(request, 'blog/feed.html', {'posts': posts})


def index(request):
    return render(request, 'blog/index.html')

def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('blog:feed')
    else:
        form = TicketForm()
    return render(request, 'blog/create_ticket.html', {'form': form})

def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)  # prends le ticket ou retourne une erreur 404 si non trouvé
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('blog:ticket_detail', ticket_id=ticket.id)  # transfert à la page de détail du ticket
    else:
        form = TicketForm(instance=ticket)  # Pré-remplir le formulaire avec les données de la critique existante
    return render(request, 'blog/edit_ticket.html', {'form': form, 'ticket': ticket})

def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        ticket.delete()  # Supprimer le ticket
        return redirect('blog:ticket_detail', ticket_id=ticket.id) # Rediriger vers la page de détail du ticket
    return render(request, 'blog/delete_ticket.html', {'ticket': ticket})


def create_review(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('blog:feed')
    else:
        form = ReviewForm()
    return render(request, 'blog/create_review.html', {'form': form, 'ticket': ticket})

def ticket_detail(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    reviews = Review.objects.filter(ticket=ticket)
    return render(request, 'blog/ticket_detail.html', {'ticket': ticket, 'reviews': reviews})

from django.shortcuts import get_object_or_404

def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)  # Get the review or return a 404 if not found
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('blog:ticket_detail', ticket_id=review.ticket.id)  # Redirect to ticket detail page
    else:
        form = ReviewForm(instance=review)  # Pre-fill the form with the existing review data
    return render(request, 'blog/edit_review.html', {'form': form, 'review': review})

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.delete()  # Delete the review
        return redirect('blog:ticket_detail', ticket_id=review.ticket.id)  # Redirect to ticket detail page
    return render(request, 'blog/delete_review.html', {'review': review})

def ticket_reviews_details(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    reviews = Review.objects.filter(ticket=ticket).order_by('-time_created')
    return render(request, 'blog/ticket_detail.html', {'ticket': ticket, 'reviews': reviews})


@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    following = UserFollows.objects.filter(user=profile_user).select_related('followed_user')
    followers = UserFollows.objects.filter(followed_user=profile_user).select_related('user')

    if request.method == 'POST':
        if 'follow' in request.POST:  # si clic 'follow'
            form = FollowUserForm(request.POST)
            if form.is_valid():
                follow = form.save(commit=False)
                follow.user = request.user
                follow.save()
                return redirect('blog:user_profile', username=username)
        elif 'unfollow' in request.POST:  # si clic 'unfollow'
            try:
                follow_instance = UserFollows.objects.get(user=request.user, followed_user=profile_user)
                follow_instance.delete()  # suppr. l'user suivi
            except UserFollows.DoesNotExist:
                pass
            return redirect('blog:user_profile', username=username)
    else:
        form = FollowUserForm()

    context_data = {
        'profile_user': profile_user,
        'following': following,
        'followers': followers,
        'form': form,
        'is_following': UserFollows.objects.filter(user=request.user, followed_user=profile_user).exists()
    }

    return render(request, 'blog/user_profile.html', context_data)