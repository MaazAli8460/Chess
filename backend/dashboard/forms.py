from django import forms

from blog.models import Article, ArticleCategory
from courses.models import Category, Lesson
from payments.models import SubscriptionPlan
from users.models import User

from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            input_type = getattr(widget, "input_type", "")

            if isinstance(widget, forms.Textarea):
                css_class = "form-control"
                widget.attrs.setdefault("rows", 4)
            elif isinstance(widget, forms.Select):
                css_class = "form-select"
            elif input_type == "checkbox":
                css_class = "form-check-input"
            else:
                css_class = "form-control"

            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} {css_class}".strip()

            if input_type != "checkbox":
                widget.attrs.setdefault("placeholder", field.label)

            if field_name == "quote":
                widget.attrs.setdefault("placeholder", "Share the impact in their own words")

    class Meta:
        model = Testimonial
        fields = ("name", "title", "quote", "rating", "is_published", "sort_order")


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = (
            "title",
            "order",
            "content",
            "video_url",
            "fen_start",
            "pgn_example",
            "is_free_preview",
            "estimated_minutes",
        )
        widgets = {"content": forms.Textarea(attrs={"rows": 8}), "pgn_example": forms.Textarea(attrs={"rows": 6})}


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "category", "author", "body", "meta_description", "is_published", "published_at")
        widgets = {"body": forms.Textarea(attrs={"rows": 14}), "meta_description": forms.Textarea(attrs={"rows": 2})}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)


class ArticleCategoryForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = ("name",)


class SubscriptionPlanForm(forms.ModelForm):
    class Meta:
        model = SubscriptionPlan
        fields = ("name", "description", "price_monthly", "stripe_price_id", "is_active")
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}


class OperationsUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "role", "is_active", "is_staff", "is_email_verified")
