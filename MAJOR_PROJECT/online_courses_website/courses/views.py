from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay
import uuid
from django.http import JsonResponse

from .models import Course, Enrollment, Payment, Faculty
from .forms import ContactForm, SignupForm

# ✅ Razorpay Client Setup
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

# ✅ Home Page
def home(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})

# ✅ About Page
def about(request):
    faculties = Faculty.objects.all()
    return render(request, 'about.html', {'faculties': faculties})

# ✅ Contact Page
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

# ✅ Login User
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

# ✅ Logout User
@login_required(login_url='/login/')
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

# ✅ Signup User
@csrf_exempt
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created! Redirecting to home page.")
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "signup.html", {'form': form})

# ✅ My Courses (Show Enrolled Courses)
@login_required(login_url='/login/')
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    return render(request, 'my_courses.html', {'courses': [e.course for e in enrollments]})

# ✅ Course Detail Page
@login_required(login_url='/login/')
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})

# ✅ Enroll in Course (Only After Payment)
@login_required(login_url='/login/')
def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # ✅ Check if payment exists and is completed
    payment = Payment.objects.filter(user=request.user, course=course, status="Completed").first()

    if payment:
        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            Enrollment.objects.create(student=request.user, course=course)
            messages.success(request, "Enrollment successful! You can now access the course.")
        else:
            messages.warning(request, "You are already enrolled in this course.")
    else:
        messages.error(request, "Payment not completed. Please make payment to enroll.")

    return redirect('course_detail', course_id=course.id)

# ✅ Initiate Payment with Razorpay
@login_required(login_url='/login/')
def initiate_payment(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # ✅ Check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.warning(request, "You are already enrolled in this course.")
        return redirect('my_courses')

    # ✅ Create a Razorpay Order
    order_amount = int(course.price * 100)  # Convert to paisa
    order_currency = 'INR'
    order_receipt = str(uuid.uuid4())  # Generate unique receipt ID

    razorpay_order = razorpay_client.order.create({
        'amount': order_amount,
        'currency': order_currency,
        'receipt': order_receipt,
        'payment_capture': '1'
    })

    # ✅ Save payment details in DB (Pending status)
    payment = Payment.objects.create(
        user=request.user,
        course=course,
        payment_id=razorpay_order['id'],
        amount=course.price,
        status='Pending'
    )

    context = {
        'course': course,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'amount': order_amount,
        'currency': order_currency
    }
    return render(request, 'payment_page.html', context)

# ✅ Verify Payment and Enroll User
@csrf_exempt
def verify_payment(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')



        try:
            payment = get_object_or_404(Payment, payment_id=razorpay_order_id)
            # ✅ Verify Razorpay Signature
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            # ✅ Update Payment Status
            payment.status = "Completed"
            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.save()

            # ✅ Enroll the student after successful payment
            Enrollment.objects.create(student=payment.user, course=payment.course,payment=payment)
            return JsonResponse({"success": True})



        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"success":False, "message": "Payment verification failed."})

    return JsonResponse({"success": False, "message":"Invalid request."})

@login_required(login_url='/login/')
def payment_success(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Ensure user is logged in
    if request.user.is_authenticated:
        # Enroll the user in the course
        Enrollment.objects.get_or_create(student=request.user, course=course)

    return redirect('my_courses')


