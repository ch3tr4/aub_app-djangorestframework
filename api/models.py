import secrets
from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

def generate_user_id():
    year = timezone.now().year
    last_user = AppUser.objects.order_by('-id').first()
    next_number = (last_user.id + 1) if last_user else 1
    return f"AUB{year}{next_number:04d}"


class AppUser(models.Model):
    user_id = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200, editable=False)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=30)
    password = models.CharField(max_length=128)  # hashed
    image = models.ImageField(upload_to='users/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # auto-generate user_id
        if not self.user_id:
            self.user_id = generate_user_id()

        # auto full name
        self.full_name = f"{self.first_name} {self.last_name}"

        # hash password once
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user_id

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    aub_id = models.CharField(max_length=20, unique=True)

    image = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )

    gender = models.CharField(
        max_length=10,
        blank=True
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    student_id = models.CharField(
        max_length=20,
        blank=True
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    def __str__(self):
        return self.aub_id

class News(models.Model):
    CATEGORY_CHOICES = (
        ('general', 'General'),
        ('events', 'Events'),
        ('announcement', 'Announcement'),
    )

    title = models.CharField(max_length=255)
    thumbnail = models.ImageField(
        upload_to='news/',
        null=True,
        blank=True
    )
    content = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='general'
    )
    views = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']




class Course(models.Model):
    course_id = models.CharField(max_length=50, unique=True)
    course_name = models.CharField(max_length=255)
    course_info = models.TextField(blank=True)

    class Meta:
        ordering = ['course_id']

    def __str__(self):
        return f"{self.course_id} - {self.course_name}"
    
class CourseInfo(models.Model):
    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='extra_courses'
    )
    program = models.CharField(max_length=255)
    price_per_semester = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_year = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['course__course_id', 'program']
        # optional: prevent duplicate program entries for same course
        unique_together = ('course', 'program')

    def __str__(self):
        return f"{self.course.course_id} | {self.program}"
    
class EventMenu(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='events/')
    event_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-event_date']

    def __str__(self):
        return self.title

class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    contact = models.CharField(max_length=255)
    telegram_link = models.URLField(blank=True, null=True)

    image = models.ImageField(
        upload_to='jobs/',
        null=True,
        blank=True
    )

    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_title = models.CharField(max_length=255)
    book_image = models.ImageField(upload_to='book_images/', blank=True, null=True)
    description = models.TextField(blank=True)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.book_title

    
class ExtraCourse(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.CharField(max_length=50)
    related_course = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to='extra_courses/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    DEGREE_CHOICES = [
        ('Associate', 'Associate'),
        ('Bachelor', 'Bachelor'),
        ('Master', 'Master'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    degree_level = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    major = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.degree_level} - {self.status}"
