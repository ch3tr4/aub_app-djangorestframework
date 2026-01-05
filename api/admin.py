from django.contrib import admin
from .models import *

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_id', 'course_name')
    search_fields = ('course_id', 'course_name')

@admin.register(CourseInfo)
class CourseInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'program', 'price_per_semester', 'price_per_year')
    list_filter = ('program',)
    search_fields = ('course__course_id', 'course__course_name', 'program')

@admin.register(EventMenu)
class EventMenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'is_active')
    list_filter = ('is_active', 'event_date')
    search_fields = ('title',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'book_title', 'views', 'created_at')
    readonly_fields = ('book_id', 'created_at')

# @admin.register(AppUser)
# class AppUserAdmin(admin.ModelAdmin):
#     list_display = ('user_id', 'full_name', 'phone_number', 'created_at')

@admin.register(ExtraCourse)
class ExtraCourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'related_course')

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_open', 'created_at')
    list_filter = ('is_open',)
    search_fields = ('title',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree_level', 'major', 'status', 'created_at')
    list_filter = ('status', 'degree_level')
    search_fields = ('user__username', 'major')