from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Choice, Course, Lesson, Question, Submission


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "lesson", "order")
    list_filter = ("lesson__course",)
    search_fields = ("question_text",)
    inlines = [ChoiceInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "order")
    list_filter = ("course",)
    search_fields = ("title",)
    inlines = [QuestionInline]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "score", "submitted_at")
    list_filter = ("course",)
    readonly_fields = ("submitted_at",)


# The imports below make the built-in authentication models available for admin
# customization if needed. Django already registers them in its default admin.
# Avoid registering them again, which would raise AlreadyRegistered.
