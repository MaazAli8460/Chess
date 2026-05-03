from django.urls import path

from .views import (
    CourseDetailApiView,
    CourseListApiView,
    course_create_view,
    course_detail_view,
    course_list_view,
    enroll_course_view,
    lesson_detail_view,
)

app_name = "courses"

urlpatterns = [
    path("", course_list_view, name="list"),
    path("create/", course_create_view, name="create"),
    path("api/courses/", CourseListApiView.as_view(), name="api-list"),
    path("api/courses/<slug:slug>/", CourseDetailApiView.as_view(), name="api-detail"),
    path("<slug:slug>/", course_detail_view, name="detail"),
    path("<slug:slug>/enroll/", enroll_course_view, name="enroll"),
    path("<slug:slug>/lessons/<int:lesson_id>/", lesson_detail_view, name="lesson"),
]
