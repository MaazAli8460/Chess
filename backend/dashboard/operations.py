from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from blog.models import Article, ArticleCategory
from courses.forms import CourseForm
from courses.models import Category, Course, Enrollment, Lesson
from payments.models import PaymentTransaction, SubscriptionPlan, UserSubscription

from .forms import (
    ArticleCategoryForm,
    ArticleForm,
    CategoryForm,
    LessonForm,
    OperationsUserForm,
    SubscriptionPlanForm,
    TestimonialForm,
)
from .models import Testimonial

User = get_user_model()
staff_operation_required = user_passes_test(lambda user: user.is_staff, login_url="login")


def _page(request, template, **context):
    return render(request, template, {"operation_section": context.pop("operation_section", "overview"), **context})


@staff_operation_required
def operation_home(request):
    recent_courses = Course.objects.select_related("created_by").order_by("-created_at")[:5]
    recent_users = User.objects.order_by("-date_joined")[:5]
    return _page(
        request,
        "operations/home.html",
        operation_section="overview",
        counts={
            "courses": Course.objects.count(),
            "published_courses": Course.objects.filter(is_published=True).count(),
            "users": User.objects.count(),
            "enrollments": Enrollment.objects.count(),
            "active_subscriptions": UserSubscription.objects.filter(status=UserSubscription.STATUS_ACTIVE).count(),
            "revenue": PaymentTransaction.objects.filter(status=PaymentTransaction.STATUS_SUCCESS).aggregate(total=Sum("amount"))["total"] or 0,
            "articles": Article.objects.count(),
        },
        recent_courses=recent_courses,
        recent_users=recent_users,
    )


@staff_operation_required
def course_list(request):
    query = request.GET.get("q", "").strip()
    courses = Course.objects.select_related("category", "created_by").all()
    if query:
        courses = courses.filter(Q(title__icontains=query) | Q(description__icontains=query))
    return _page(request, "operations/courses.html", operation_section="courses", courses=courses, query=query)


@staff_operation_required
def course_create(request):
    form = CourseForm(request.POST or None)
    if form.is_valid():
        course = form.save(commit=False)
        course.created_by = request.user
        course.save()
        messages.success(request, f"{course.title} is ready for lessons.")
        return redirect("dashboard:operations-course-edit", course_id=course.id)
    return _page(request, "operations/form.html", operation_section="courses", form=form, title="Create course", eyebrow="Course studio", back_url="dashboard:operations-courses")


@staff_operation_required
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    form = CourseForm(request.POST or None, instance=course)
    if form.is_valid():
        form.save()
        messages.success(request, "Course details updated.")
        return redirect("dashboard:operations-course-edit", course_id=course.id)
    return _page(
        request,
        "operations/course_edit.html",
        operation_section="courses",
        form=form,
        course=course,
        lessons=course.lessons.all(),
    )


@staff_operation_required
def lesson_create(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    form = LessonForm(request.POST or None)
    if form.is_valid():
        lesson = form.save(commit=False)
        lesson.course = course
        lesson.save()
        messages.success(request, "Lesson added to the course.")
        return redirect("dashboard:operations-course-edit", course_id=course.id)
    return _page(request, "operations/form.html", operation_section="courses", form=form, title="Add lesson", eyebrow=course.title, back_url="dashboard:operations-course-edit", back_id=course.id)


@staff_operation_required
def lesson_edit(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    form = LessonForm(request.POST or None, instance=lesson)
    if form.is_valid():
        form.save()
        messages.success(request, "Lesson updated.")
        return redirect("dashboard:operations-course-edit", course_id=course.id)
    return _page(request, "operations/form.html", operation_section="courses", form=form, title="Edit lesson", eyebrow=course.title, back_url="dashboard:operations-course-edit", back_id=course.id)


@staff_operation_required
@require_POST
def lesson_delete(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    lesson.delete()
    messages.success(request, "Lesson removed.")
    return redirect("dashboard:operations-course-edit", course_id=course.id)


@staff_operation_required
def category_list(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Course category added.")
        return redirect("dashboard:operations-categories")
    return _page(request, "operations/categories.html", operation_section="categories", form=form, categories=Category.objects.all(), article_categories=ArticleCategory.objects.all())


@staff_operation_required
def users_list(request):
    query = request.GET.get("q", "").strip()
    users = User.objects.all()
    if query:
        users = users.filter(Q(username__icontains=query) | Q(email__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
    return _page(request, "operations/users.html", operation_section="users", users=users, query=query)


@staff_operation_required
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = OperationsUserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, f"{user.username}'s account was updated.")
        return redirect("dashboard:operations-users")
    return _page(request, "operations/form.html", operation_section="users", form=form, title=f"Edit {user.username}", eyebrow="Account operations", back_url="dashboard:operations-users")


@staff_operation_required
def article_list(request):
    query = request.GET.get("q", "").strip()
    articles = Article.objects.select_related("author", "category").all()
    if query:
        articles = articles.filter(Q(title__icontains=query) | Q(body__icontains=query))
    return _page(request, "operations/articles.html", operation_section="articles", articles=articles, query=query)


@staff_operation_required
def article_edit(request, article_id=None):
    article = get_object_or_404(Article, id=article_id) if article_id else None
    form = ArticleForm(request.POST or None, instance=article)
    if not article and not request.POST:
        form.initial["author"] = request.user.id
    if form.is_valid():
        article = form.save(commit=False)
        if article.is_published and not article.published_at:
            article.published_at = timezone.now()
        if not article.is_published:
            article.published_at = None
        article.save()
        messages.success(request, "Article saved.")
        return redirect("dashboard:operations-articles")
    return _page(request, "operations/form.html", operation_section="articles", form=form, title="Edit article" if article else "Write article", eyebrow="Content studio", back_url="dashboard:operations-articles")


@staff_operation_required
@require_POST
def article_delete(request, article_id):
    get_object_or_404(Article, id=article_id).delete()
    messages.success(request, "Article deleted.")
    return redirect("dashboard:operations-articles")


@staff_operation_required
def article_categories(request):
    form = ArticleCategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Article category added.")
        return redirect("dashboard:operations-article-categories")
    return _page(request, "operations/categories.html", operation_section="article-categories", form=form, categories=Category.objects.none(), article_categories=ArticleCategory.objects.all(), article_mode=True)


@staff_operation_required
def testimonial_list(request):
    form = TestimonialForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Testimonial saved.")
        return redirect("dashboard:operations-testimonials")
    return _page(request, "operations/testimonials.html", operation_section="testimonials", form=form, testimonials=Testimonial.objects.all())


@staff_operation_required
def testimonial_edit(request, testimonial_id):
    testimonial = get_object_or_404(Testimonial, id=testimonial_id)
    form = TestimonialForm(request.POST or None, request.FILES or None, instance=testimonial)
    if form.is_valid():
        form.save()
        messages.success(request, "Testimonial updated.")
        return redirect("dashboard:operations-testimonials")
    return _page(request, "operations/form.html", operation_section="testimonials", form=form, title="Edit testimonial", eyebrow="Social proof", back_url="dashboard:operations-testimonials")


@staff_operation_required
@require_POST
def testimonial_delete(request, testimonial_id):
    get_object_or_404(Testimonial, id=testimonial_id).delete()
    messages.success(request, "Testimonial deleted.")
    return redirect("dashboard:operations-testimonials")


@staff_operation_required
def plan_list(request):
    form = SubscriptionPlanForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Subscription plan saved.")
        return redirect("dashboard:operations-plans")
    return _page(request, "operations/plans.html", operation_section="billing", form=form, plans=SubscriptionPlan.objects.all(), subscriptions=UserSubscription.objects.select_related("user", "plan")[:20])


@staff_operation_required
def plan_edit(request, plan_id):
    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    form = SubscriptionPlanForm(request.POST or None, instance=plan)
    if form.is_valid():
        form.save()
        messages.success(request, "Subscription plan updated.")
        return redirect("dashboard:operations-plans")
    return _page(request, "operations/form.html", operation_section="billing", form=form, title=f"Edit {plan.name}", eyebrow="Billing", back_url="dashboard:operations-plans")


@staff_operation_required
def payment_list(request):
    payments = PaymentTransaction.objects.select_related("user").all()[:100]
    return _page(request, "operations/payments.html", operation_section="payments", payments=payments)
