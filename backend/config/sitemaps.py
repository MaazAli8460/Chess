from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from blog.models import Article
from courses.models import Course


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return ["dashboard:home", "courses:list", "blog:list"]

    def location(self, item):
        return reverse(item)


class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Course.objects.filter(is_published=True)

    def location(self, obj):
        return reverse("courses:detail", args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Article.objects.filter(is_published=True)

    def location(self, obj):
        return reverse("blog:detail", args=[obj.slug])

    def lastmod(self, obj):
        return obj.updated_at
