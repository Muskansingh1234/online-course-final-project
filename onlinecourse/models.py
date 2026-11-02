
from django.conf import settings
from django.db import models


class Instructor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    full_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.full_name


class Learner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.full_name


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    instructors = models.ManyToManyField(Instructor, blank=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, related_name="lessons", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.course.name}: {self.title}"


class Enrollment(models.Model):
    learner = models.ForeignKey(
        Learner, on_delete=models.CASCADE, related_name="enrollments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    date_enrolled = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.learner} - {self.course}"


class Question(models.Model):
    course = models.ForeignKey(
        Course, related_name="questions", on_delete=models.CASCADE
    )
    content = models.TextField()
    grade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.content[:80]

    def is_get_score(self, selected_ids):
        correct_ids = set(
            self.choices.filter(is_correct=True).values_list("id", flat=True)
        )
        selected_ids = {int(choice_id) for choice_id in selected_ids}
        return bool(correct_ids) and correct_ids == selected_ids


class Choice(models.Model):
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )
    choice_text = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(
        Enrollment, related_name="submissions", on_delete=models.CASCADE
    )
    choices = models.ManyToManyField(Choice, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Submission {self.id} - {self.enrollment}"
