from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Reservation, Feedback
from .forms import ReservationForm, FeedbackForm

def home(request):
    return render(request, 'restaurant/home.html')

def menu(request):
    return render(request, 'restaurant/menu.html')

def about(request):
    return render(request, 'restaurant/about.html')

def reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your reservation has been made successfully!")
            return redirect("reservation")
    else:
        form = ReservationForm()
    return render(request, 'restaurant/reservation.html', {'form': form})

def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect("feedback")
    else:
        form = FeedbackForm()
    return render(request, 'restaurant/feedback.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")  # Use get() to prevent KeyError
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect("home")  # Redirect to home page after successful login
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "restaurant/login.html")

def user_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")  # Redirect to login page after successful registration
    else:
        form = UserCreationForm()

    return render(request, 'restaurant/register.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")  # Redirect to login after logout
