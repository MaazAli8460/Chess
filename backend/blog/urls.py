from django.urls import path

from .views import article_detail_view, article_list_view

app_name = "blog"

urlpatterns = [
    path("", article_list_view, name="list"),
    path("<slug:slug>/", article_detail_view, name="detail"),
]
