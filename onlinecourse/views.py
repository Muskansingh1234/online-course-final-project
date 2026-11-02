from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Choice, Course, Question, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, "onlinecourse/course_details_bootstrap.html", {"course": course})


@login_required
def exam(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = Question.objects.filter(lesson__course=course).prefetch_related("choices")
    return render(request, "onlinecourse/exam.html", {"course": course, "questions": questions})


@login_required
def submit(request, course_id):
    if request.method != "POST":
        return redirect("onlinecourse:exam", course_id=course_id)

    course = get_object_or_404(Course, pk=course_id)
    questions = list(
        Question.objects.filter(lesson__course=course).prefetch_related("choices")
    )
    total = len(questions)
    correct = 0
    answers = []

    for question in questions:
        selected_id = request.POST.get(f"question_{question.id}")
        selected = None
        if selected_id:
            selected = Choice.objects.filter(
                pk=selected_id, question=question
            ).first()
        is_correct = bool(selected and selected.is_correct)
        if is_correct:
            correct += 1
        answers.append({
            "question": question,
            "selected": selected,
            "is_correct": is_correct,
            "correct_choice": question.choices.filter(is_correct=True).first(),
        })

    score = round((correct / total) * 100) if total else 0
    submission = Submission.objects.create(
        student=request.user,
        course=course,
        score=score,
        total_questions=total,
        correct_answers=correct,
    )
    request.session[f"submission_{submission.id}_answers"] = [
        {
            "question": a["question"].question_text,
            "selected": a["selected"].choice_text if a["selected"] else "Not answered",
            "correct": a["correct_choice"].choice_text if a["correct_choice"] else "Not configured",
            "is_correct": a["is_correct"],
        } for a in answers
    ]
    return redirect("onlinecourse:show_exam_result", submission_id=submission.id)


@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id, student=request.user)
    answers = request.session.get(f"submission_{submission.id}_answers", [])
    return render(request, "onlinecourse/result.html", {
        "submission": submission,
        "answers": answers,
        "passed": submission.score >= 70,
    })
