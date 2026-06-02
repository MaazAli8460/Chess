"""URL routing for the Chess Learning Platform."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import include, path

from config.sitemaps import BlogSitemap, CourseSitemap, StaticViewSitemap
from dashboard.admin_views import analytics_dashboard

sitemaps = {
    "static": StaticViewSitemap,
    "courses": CourseSitemap,
    "blog": BlogSitemap,
}


def robots_txt(request):
    content = render_to_string("robots.txt")
    return HttpResponse(content, content_type="text/plain")


urlpatterns = [
    # Admin analytics must come before the main admin site URL
    path("admin/analytics/", analytics_dashboard, name="admin-analytics"),
    path("admin/", admin.site.urls),

    path("robots.txt", robots_txt),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),

    path("", include("dashboard.urls")),
    path("users/", include("users.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("courses/", include("courses.urls")),
    path("chess/", include("chesslab.urls")),
    path("payments/", include("payments.urls")),
    path("blog/", include("blog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
