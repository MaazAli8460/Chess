from django.urls import path

from .views import AnalyzePositionApiView, CheckMoveApiView, EngineMoveApiView, analyzer_view, import_games_view, play_view

app_name = "chesslab"

urlpatterns = [
    path("analyzer/", analyzer_view, name="analyzer"),
    path("play/", play_view, name="play"),
    path("games/", import_games_view, name="import-games"),
    path("api/analyze/", AnalyzePositionApiView.as_view(), name="api-analyze"),
    path("api/check-move/", CheckMoveApiView.as_view(), name="api-check-move"),
    path("api/engine-move/", EngineMoveApiView.as_view(), name="api-engine-move"),
]
