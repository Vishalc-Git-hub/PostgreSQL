from django.db import models

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent_category = models.ForeignKey('self', null=True, blank=True,
                                        on_delete=models.SET_NULL, related_name='children')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name


class Course(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('All Levels', 'All Levels'),
    ]

    course_id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='courses')
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=50, default='English')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='All Levels')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    thumbnail_url = models.CharField(max_length=500, blank=True, null=True)
    promo_video_url = models.CharField(max_length=500, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # fixed 'at' typo

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return self.title


class Section(models.Model):
    section_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order_index = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sections'
        ordering = ['order_index']

    def __str__(self):
        return f"{self.course.title} — {self.title}"


class Lecture(models.Model):
    lecture_id = models.AutoField(primary_key=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video_url = models.CharField(max_length=500, blank=True, null=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    order_index = models.IntegerField()
    is_preview = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lectures'
        ordering = ['order_index']

    def __str__(self):
        return f"{self.section.title} — {self.title}"


class Resource(models.Model):
    resource_id = models.AutoField(primary_key=True)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=255)
    file_url = models.CharField(max_length=500)
    file_type = models.CharField(max_length=50, blank=True, null=True)
    file_size_kb = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'resources'

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    price_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'enrollments'
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} -> {self.course}"


class LectureProgress(models.Model):
    progress_id = models.AutoField(primary_key=True)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lecture_progress')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    last_watched_second = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'lecture_progress'
        unique_together = ('enrollment', 'lecture')

    def __str__(self):
        return f"Progress: {self.enrollment} - {self.lecture}"


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return f"Review {self.rating} by {self.enrollment.user}"


class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart_items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cart_items')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_items'
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} - {self.course}"


class Certificate(models.Model):
    certificate_id = models.AutoField(primary_key=True)
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    certificate_url = models.CharField(max_length=500, blank=True, null=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'certificates'

    def __str__(self):
        return f"Certificate for {self.enrollment}"

