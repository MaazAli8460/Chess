from django.urls import path

from .views import AnalyzePositionApiView, analyzer_view, import_games_view, play_view

app_name = "chesslab"

urlpatterns = [
    path("analyzer/", analyzer_view, name="analyzer"),
    path("play/", play_view, name="play"),
    path("games/", import_games_view, name="import-games"),
    path("api/analyze/", AnalyzePositionApiView.as_view(), name="api-analyze"),
]
