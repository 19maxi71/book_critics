from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView


# urlpatterns = [
#     path("", views.index, name="index"),
# ]

app_name = "blog"

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path("feed/", views.feed, name="feed"),
    path('', views.index, name='index'),
    path("create_ticket/", views.create_ticket, name="create_ticket"),
    path("create_review/<int:ticket_id>/", views.create_review, name="create_review"),
    path("ticket_detail/<int:ticket_id>/", views.ticket_detail, name="ticket_detail"),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('ticket_reviews_details/<int:ticket_id>/', views.ticket_reviews_details, name='ticket_reviews_details'),
    path('edit_ticket/<int:ticket_id>/', views.edit_ticket, name='edit_ticket'),
    path('delete_ticket/<int:ticket_id>/', views.delete_ticket, name='delete_ticket'),
    path('user_profile/<str:username>/', views.user_profile, name='user_profile'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='blog/logout'),
]
