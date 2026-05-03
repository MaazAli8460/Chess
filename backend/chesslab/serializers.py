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
