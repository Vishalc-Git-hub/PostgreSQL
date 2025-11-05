from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    CategoryViewSet, CourseViewSet, SectionViewSet, LectureViewSet, ResourceViewSet,
    EnrollmentViewSet, LectureProgressViewSet, ReviewViewSet, CartItemViewSet, CertificateViewSet
)

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('courses', CourseViewSet)
router.register('sections', SectionViewSet)
router.register('lectures', LectureViewSet)
router.register('resources', ResourceViewSet)
router.register('enrollments', EnrollmentViewSet)
router.register('lecture-progress', LectureProgressViewSet, basename='lecture-progress')
router.register('reviews', ReviewViewSet)
router.register('cart-items', CartItemViewSet)
router.register('certificates', CertificateViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
