from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Value, CharField
from .models import Review, Ticket, UserFollows
from itertools import chain
from django.contrib.auth.forms import UserCreationForm
from .forms import TicketForm, ReviewForm, FollowUserForm, UserSearchForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.urls import reverse


def register(request):
    """
    Vue pour l'inscription d'un nouvel utilisateur.
    """
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


@login_required
def feed(request):
    """
    Vue pour afficher le feed des tickets et des critiques des utilisateurs suivis.
    """
    following_users = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)
    reviews = Review.objects.filter(user__in=following_users) | Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = Ticket.objects.filter(user__in=following_users) | Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # Créer un dictionnaire pour stocker la dernière critique pour chaque ticket
    latest_reviews = {}
    for review in reviews:
        if review.ticket.id not in latest_reviews or review.time_created > latest_reviews[review.ticket.id].time_created:
            latest_reviews[review.ticket.id] = review

    # Combiner les tickets et leurs dernières critiques dans une seule liste
    posts = []
    for ticket in tickets:
        if ticket.id in latest_reviews:
            posts.append(latest_reviews[ticket.id])
        posts.append(ticket)

    # Trier la liste combinée par date de création
    posts = sorted(posts, key=lambda post: post.time_created, reverse=True)

    return render(request, 'blog/feed.html', {'posts': posts})


def index(request):
    """
    Vue pour la page d'accueil.
    """
    return render(request, 'blog/index.html')


@login_required
def create_ticket(request):
    """
    Vue pour créer un nouveau ticket.
    """
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


@login_required
def edit_ticket(request, ticket_id):
    """
    Vue pour éditer un ticket existant.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier ce ticket.")
    
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('blog:ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'blog/edit_ticket.html', {'form': form, 'ticket': ticket})


@login_required
def delete_ticket(request, ticket_id):
    """
    Vue pour supprimer un ticket existant.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer ce ticket.")
    
    if request.method == 'POST':
        ticket.delete()
        return redirect('blog:ticket_detail', ticket_id=ticket.id)
    return render(request, 'blog/delete_ticket.html', {'ticket': ticket})


@login_required
def create_review(request, ticket_id):
    """
    Vue pour créer une nouvelle critique pour un ticket existant.
    """
    ticket = Ticket.objects.get(id=ticket_id)
    
    if Review.objects.filter(user=request.user, ticket=ticket).exists():
        messages.error(request, "Vous avez déjà critiqué ce ticket.")
        # Rediriger vers les détails du ticket si l'utilisateur a déjà critiqué le ticket
        return redirect(reverse('blog:ticket_detail', args=[ticket.id]))
    
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
    """
    Vue pour afficher les détails d'un ticket et ses critiques associées.
    """
    ticket = Ticket.objects.get(id=ticket_id)
    reviews = Review.objects.filter(ticket=ticket)
    return render(request, 'blog/ticket_detail.html', {'ticket': ticket, 'reviews': reviews})


@login_required
def edit_review(request, review_id):
    """
    Vue pour éditer une critique existante.
    """
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier cette critique.")
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('blog:ticket_detail', ticket_id=review.ticket.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'blog/edit_review.html', {'form': form, 'review': review})


@login_required
def delete_review(request, review_id):
    """
    Vue pour supprimer une critique existante.
    """
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer cette critique.")
    
    if request.method == 'POST':
        review.delete()
        return redirect('blog:ticket_detail', ticket_id=review.ticket.id)
    return render(request, 'blog/delete_review.html', {'review': review})


def ticket_reviews_details(request, ticket_id):
    """
    Vue pour afficher les détails d'un ticket et ses critiques, triées par date de création.
    """
    ticket = Ticket.objects.get(id=ticket_id)
    reviews = Review.objects.filter(ticket=ticket).order_by('-time_created')
    return render(request, 'blog/ticket_detail.html', {'ticket': ticket, 'reviews': reviews})


@login_required
def user_profile(request, username):
    """
    Vue pour afficher le profil utilisateur et gérer les abonnements.
    """
    profile_user = get_object_or_404(User, username=username)
    if request.user != profile_user:
        return HttpResponseForbidden("ACCÈS REFUSÉ")
    
    following = UserFollows.objects.filter(user=profile_user).select_related('followed_user')
    followers = UserFollows.objects.filter(followed_user=profile_user).select_related('user')

    search_form = UserSearchForm(request.GET or None)
    search_results = []
    if search_form.is_valid() and 'username' in search_form.cleaned_data:
        search_query = search_form.cleaned_data['username']
        search_results = User.objects.filter(username__icontains=search_query).exclude(id=profile_user.id)

    if request.method == 'POST':
        if 'follow' in request.POST:  # Bouton "Suivre" pressé
            form = FollowUserForm(request.POST)
            if form.is_valid():
                follow = form.save(commit=False)
                follow.user = request.user
                try:
                    follow.save()
                except IntegrityError:
                    messages.error(request, 'Vous suivez déjà cet utilisateur.')
                return redirect('blog:user_profile', username=username)
        elif 'unfollow' in request.POST:  # Bouton "Ne plus suivre" pressé
            try:
                follow_instance = UserFollows.objects.get(user=request.user, followed_user_id=request.POST['user_id'])
                follow_instance.delete()
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
        'search_form': search_form,
        'search_results': search_results,
        'is_following': UserFollows.objects.filter(user=request.user, followed_user=profile_user).exists()
    }

    return render(request, 'blog/user_profile.html', context_data)


@login_required
def create_critique(request):
    """
    Vue pour créer une critique et un ticket en même temps.
    """
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect('blog:feed')
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(request, 'blog/create_critique.html', {
        'ticket_form': ticket_form,
        'review_form': review_form
    })


@login_required
def user_posts(request):
    """
    Vue pour afficher les posts (tickets et critiques) de l'utilisateur connecté.
    """
    reviews = Review.objects.filter(user=request.user).annotate(content_type=Value('REVIEW', CharField()))
    tickets = Ticket.objects.filter(user=request.user).annotate(content_type=Value('TICKET', CharField()))
    
    posts = sorted(chain(reviews, tickets), key=lambda post: post.time_created, reverse=True)
    
    return render(request, 'blog/user_posts.html', {'posts': posts})