from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Course, Enrollment, Faculty
from .forms import ContactForm, SignupForm


# ✅ Fixed: Redirects users properly to login or signup
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect logged-in users to home

    if not User.objects.exists():  # If no users exist, go to signup page
        return redirect('signup')

    return redirect('login')  # Otherwise, show login page


def home(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})


def about(request):
    faculties = Faculty.objects.all()
    return render(request, 'about.html', {'faculties': faculties})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Message sent!")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


# ✅ Fixed: Simplified login function
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")
        messages.error(request, "Invalid credentials")
    return render(request, "registration/login.html")


@login_required(login_url='/login/')  # ✅ Fixed: Added `login_url`
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


# ✅ Fixed: Signup function now logs in the user after signup
@csrf_exempt
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto login after signup
            messages.success(request, "Account created! Redirecting to home page.")
            return redirect("login")
    else:
        form = SignupForm()

    return render(request, "signup.html", {'form': form})


@login_required(login_url='/login/')  # ✅ Fixed: Added `login_url`
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, "Already enrolled!")
    else:
        Enrollment.objects.create(student=request.user, course=course)
        messages.success(request, f"Enrolled in {course.title}!")
    return redirect('my_courses')


@login_required(login_url='/login/')  # ✅ Fixed: Added `login_url`
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    return render(request, 'my_courses.html', {'courses': [e.course for e in enrollments]})


@login_required(login_url='/login/')  # ✅ Fixed: Added `login_url`
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})
