from django.db import models
from django.contrib.auth.models import User


# Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " - " + self.subject


# Course Model
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/', default='default.jpeg')  # Course Image
    video_link = models.URLField(blank=True, null=True)  # Video URL
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Course Price

    def __str__(self):
        return self.title

    def enrolled_students_count(self):
        return self.enrollments.count()  # Get total enrolled students


# Course Modules
class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


# ✅ Payment Model (Linked to Razorpay Transactions)
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, unique=True)  # ✅ Ensure unique payment ID
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)  # ✅ Store Razorpay payment ID
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)  # ✅ Store Razorpay signature
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"



# Enrollment Model (Linked to Payment)
class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)  # Enrollment timestamp
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, null=True, blank=True)  # Link to Payment

    class Meta:
        unique_together = ('student', 'course')  # Prevent duplicate enrollments

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"


# User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# Faculty Model
class Faculty(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='faculty_images/', default='default.jpg')

    def __str__(self):
        return self.name
