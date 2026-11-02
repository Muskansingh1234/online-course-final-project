from django.urls import path
from . import views

app_name = "onlinecourse"

urlpatterns = [
    path("courses/<int:course_id>/", views.course_details, name="course_details"),
    path("courses/<int:course_id>/exam/", views.exam, name="exam"),
    path("submit/<int:course_id>/", views.submit, name="submit"),
    path("results/<int:submission_id>/", views.show_exam_result, name="show_exam_result"),
]
