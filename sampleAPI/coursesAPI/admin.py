from django.contrib import admin

from django.contrib import admin
from .models import (
    Category, Course, Section, Lecture, Resource,
    Enrollment, LectureProgress, Review, CartItem, Certificate
)

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Lecture)
admin.site.register(Resource)
admin.site.register(Enrollment)
admin.site.register(LectureProgress)
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(Certificate)

