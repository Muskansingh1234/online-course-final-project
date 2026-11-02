# Online Course – Final Project

A runnable Django starter implementation for the assessment submission tasks.

## Setup
1. Use Python 3.10+.
2. Create and activate a virtual environment.
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py makemigrations onlinecourse`
5. Run: `python manage.py migrate`
6. Create an admin user: `python manage.py createsuperuser`
7. Start the server: `python manage.py runserver`
8. Visit `http://127.0.0.1:8000/admin/`.

## Add sample course content
In Django admin, create a Course, add Lessons, and add Questions with Choices.
Mark the correct Choice for each Question. The exam page is available at
`/courses/<course_id>/exam/` and the result page follows a successful submission.

## Assignment evidence
- Task 1: `onlinecourse/models.py`
- Task 2: `onlinecourse/admin.py`
- Task 3: take a screenshot of `/admin/` showing both Authentication and Authorization
  and OnlineCourse sections. Save it as `03-admin-site.png`.
- Task 4: `onlinecourse/templates/onlinecourse/course_details_bootstrap.html`
- Task 5: `onlinecourse/views.py`
- Task 6: `onlinecourse/urls.py`
- Task 7: complete a mock exam with a passing score, then capture the result page,
  including the Congratulations message, score, and exam results. Save as `07-final.png`.

## Publish to GitHub
Create a **public** GitHub repository, upload this project, then use GitHub's file view
to copy the permanent public URLs for the five requested source files. Do not submit
local file paths or guessed URLs.

This is a complete starter implementation, but compare it with your course lab's exact
specifications before submitting. The screenshots must be captured from your own run.
