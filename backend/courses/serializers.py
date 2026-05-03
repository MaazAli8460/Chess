from rest_framework import serializers

from .models import Course, Lesson


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
    lessons = LessonSerializer(many=True, read_only=True)
    created_by = serializers.StringRelatedField()

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
