from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Article, ArticleCategory


def article_list_view(request: HttpRequest) -> HttpResponse:
    articles = Article.objects.filter(is_published=True).select_related("author", "category")
    categories = ArticleCategory.objects.all()

    category_slug = request.GET.get("category")
    active_category = None
    if category_slug:
        active_category = get_object_or_404(ArticleCategory, slug=category_slug)
        articles = articles.filter(category=active_category)

    paginator = Paginator(articles, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "blog/article_list.html",
        {
            "page_obj": page_obj,
            "categories": categories,
            "active_category": active_category,
        },
    )


def article_detail_view(request: HttpRequest, slug: str) -> HttpResponse:
    article = get_object_or_404(Article, slug=slug, is_published=True)
    related = (
        Article.objects.filter(is_published=True, category=article.category)
        .exclude(pk=article.pk)
        .select_related("author")[:3]
    )
    return render(
        request,
        "blog/article_detail.html",
        {"article": article, "related": related},
    )
