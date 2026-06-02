import chess
from rest_framework import serializers


class AnalyzeRequestSerializer(serializers.Serializer):
    fen = serializers.CharField(required=False, allow_blank=True)

    def validate_fen(self, value: str) -> str:
        fen = value.strip() or chess.STARTING_FEN
        try:
            chess.Board(fen)
        except ValueError as exc:
            raise serializers.ValidationError("Invalid FEN string.") from exc
        return fen


class CheckMoveSerializer(serializers.Serializer):
    fen = serializers.CharField()
    move = serializers.CharField(help_text="Move in UCI format, e.g. 'e2e4'")

    def validate_fen(self, value: str) -> str:
        try:
            chess.Board(value.strip())
        except ValueError as exc:
            raise serializers.ValidationError("Invalid FEN string.") from exc
        return value.strip()

    def validate_move(self, value: str) -> str:
        return value.strip().lower()


class EngineMoveSerializer(serializers.Serializer):
    fen = serializers.CharField()
    depth = serializers.IntegerField(default=5, min_value=1, max_value=15)

    def validate_fen(self, value: str) -> str:
        try:
            chess.Board(value.strip())
        except ValueError as exc:
            raise serializers.ValidationError("Invalid FEN string.") from exc
        return value.strip()
