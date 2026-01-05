# api/urls.py
from django.urls import path, include
from rest_framework import routers
from api.views import *

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'course-info', CourseInfoViewSet, basename='course-info')
router.register(r'event-menu', EventMenuViewSet, basename='event-menu')
router.register(r'jobs', JobPostingViewSet, basename='jobs')
router.register(r'books', BookViewSet, basename='books')
router.register(r'extra-courses', ExtraCourseViewSet, basename='extra-courses')
router.register(r'enrollment', EnrollmentViewSet, basename='enrollment')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPIView.as_view(), name='app-register'),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("profile/", ProfileAPIView.as_view()),
    path("update-profile-image/", UpdateProfileImageAPIView.as_view()),
    path("change-phone/", ChangePhoneNumberAPIView.as_view()), 
    path("change-password/", ChangePasswordAPIView.as_view()), 
]
