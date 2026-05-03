from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from courses.models import Category, Course, Lesson
from payments.models import SubscriptionPlan


class Command(BaseCommand):
    help = "Create demo data for the Chess Learning Platform MVP."

    def handle(self, *args, **options):
        user_model = get_user_model()

        admin_user, _ = user_model.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "role": "admin",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin_user.set_password("admin12345")
        admin_user.role = "admin"
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

        instructor, _ = user_model.objects.get_or_create(
            username="instructor",
            defaults={
                "email": "instructor@example.com",
                "role": "instructor",
                "is_staff": True,
            },
        )
        instructor.set_password("instructor123")
        instructor.role = "instructor"
        instructor.is_staff = True
        instructor.save()

        student, _ = user_model.objects.get_or_create(
            username="student",
            defaults={
                "email": "student@example.com",
                "role": "student",
            },
        )
        student.set_password("student123")
        student.role = "student"
        student.save()

        beginner, _ = Category.objects.get_or_create(name="Beginner Path")
        tactics, _ = Category.objects.get_or_create(name="Tactics")

        free_course, _ = Course.objects.get_or_create(
            title="Chess Fundamentals",
            defaults={
                "description": "Learn board control, piece development, and basic mating patterns.",
                "category": beginner,
                "difficulty": Course.BEGINNER,
                "price": Decimal("0.00"),
                "is_published": True,
                "created_by": instructor,
            },
        )

        premium_course, _ = Course.objects.get_or_create(
            title="Winning Middlegame Plans",
            defaults={
                "description": "Build positional understanding and tactical awareness for fast improvement.",
                "category": tactics,
                "difficulty": Course.INTERMEDIATE,
                "price": Decimal("19.00"),
                "is_published": True,
                "created_by": instructor,
            },
        )

        lessons_data = [
            (
                free_course,
                [
                    (1, "Opening Principles", "Control the center and develop pieces before attacks.", True),
                    (2, "Tactical Patterns", "Spot forks, pins, skewers, and discovered attacks quickly.", False),
                    (3, "Basic Endgames", "Convert winning king-and-pawn positions confidently.", False),
                ],
            ),
            (
                premium_course,
                [
                    (1, "Imbalances and Plans", "Use pawn structure and minor piece strengths to build plans.", False),
                    (2, "Attack the King", "Launch coordinated attacks with accurate timing.", False),
                    (3, "Defensive Technique", "Neutralize threats and transition to favorable endgames.", False),
                ],
            ),
        ]

        for course, lesson_entries in lessons_data:
            for order, title, content, is_preview in lesson_entries:
                Lesson.objects.get_or_create(
                    course=course,
                    order=order,
                    defaults={
                        "title": title,
                        "content": content,
                        "is_free_preview": is_preview,
                        "estimated_minutes": 12,
                    },
                )

        SubscriptionPlan.objects.get_or_create(
            name="Pro Monthly",
            defaults={
                "description": "Access premium courses and advanced analysis features.",
                "price_monthly": Decimal("14.99"),
                "is_active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS("Demo data created successfully."))
        self.stdout.write("Credentials:")
        self.stdout.write("- admin / admin12345")
        self.stdout.write("- instructor / instructor123")
        self.stdout.write("- student / student123")
