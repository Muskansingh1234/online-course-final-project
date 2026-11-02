from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import (
    Course,
    Enrollment,
    Question,
    Choice,
    Submission,
)


def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    lessons = course.lesson_set.all()

    context = {
        "course": course,
        "lessons": lessons,
    }

    return render(
        request,
        "onlinecourse/course_details_bootstrap.html",
        context
    )


@login_required
def exam(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    questions = Question.objects.filter(
        course=course
    ).prefetch_related("choices")

    context = {
        "course": course,
        "questions": questions,
    }

    return render(
        request,
        "onlinecourse/exam_bootstrap.html",
        context
    )


@login_required
@require_POST
def submit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    enrollment = get_object_or_404(
        Enrollment,
        learner__email=request.user.email,
        course=course,
        is_active=True
    )

    questions = Question.objects.filter(course=course)

    submission = Submission.objects.create(
        enrollment=enrollment
    )

    total_score = 0

    for question in questions:
        selected_choice_ids = request.POST.getlist(
            f"question_{question.id}"
        )

        selected_choices = Choice.objects.filter(
            id__in=selected_choice_ids,
            question=question
        )

        submission.choices.add(*selected_choices)

        if question.is_get_score(selected_choice_ids):
            total_score += question.grade

    submission.score = total_score
    submission.save()

    return redirect(
        "onlinecourse:show_exam_result",
        course_id=course.id,
        submission_id=submission.id
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, id=course_id)

    enrollment = get_object_or_404(
        Enrollment,
        learner__email=request.user.email,
        course=course
    )

    submission = get_object_or_404(
        Submission,
        id=submission_id,
        enrollment=enrollment
    )

    questions = Question.objects.filter(
        course=course
    ).prefetch_related("choices")

    context = {
        "course": course,
        "submission": submission,
        "questions": questions,
        "score": submission.score,
        "total_questions": questions.count(),
    }

    return render(
        request,
        "onlinecourse/exam_result_bootstrap.html",
        context
    )