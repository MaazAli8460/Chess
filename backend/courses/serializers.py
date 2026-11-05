from rest_framework import serializers

from payments.models import UserSubscription

from .models import Course, Enrollment, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "order",
            "content",
            "video_url",
            "fen_start",
            "pgn_example",
            "estimated_minutes",
        )


class CourseSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()
    created_by = serializers.StringRelatedField()

    def get_lessons(self, course):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        can_access = not course.is_premium
        if user and user.is_authenticated:
            can_access = (
                Enrollment.objects.filter(student=user, course=course).exists()
                or UserSubscription.objects.filter(
                    user=user,
                    status=UserSubscription.STATUS_ACTIVE,
                ).exists()
            )
        if not can_access:
            return []
        return LessonSerializer(course.lessons.all(), many=True).data

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "difficulty",
            "price",
            "is_premium",
            "is_published",
            "created_by",
            "lessons",
        )
