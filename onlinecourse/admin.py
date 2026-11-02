from django.contrib import admin
from .models import (
    Course,
    Lesson,
    Instructor,
    Learner,
    Question,
    Choice,
    Submission,
)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    inlines = [QuestionInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("content", "course", "grade")
    list_filter = ("course",)
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("choice_text", "question", "is_correct")
    list_filter = ("is_correct",)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("full_name",)


@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "enrollment", "submitted_at")