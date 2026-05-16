from django.contrib import admin
from django.utils import timezone

from .models import Article, ArticleCategory


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.action(description="Publish selected articles")
def publish_articles(modeladmin, request, queryset):
    queryset.update(is_published=True, published_at=timezone.now())


@admin.action(description="Unpublish selected articles")
def unpublish_articles(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "is_published", "published_at")
    list_filter = ("is_published", "category")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    actions = [publish_articles, unpublish_articles]
    raw_id_fields = ("author",)
    fieldsets = (
        (None, {"fields": ("title", "slug", "author", "category", "body")}),
        ("SEO", {"fields": ("meta_description",)}),
        ("Publishing", {"fields": ("is_published", "published_at")}),
    )
