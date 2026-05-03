from pathlib import Path

import chess
import chess.engine
from django.conf import settings


def _material_score(board: chess.Board) -> int:
    values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
    }
    score = 0
    for piece_type, value in values.items():
        score += len(board.pieces(piece_type, chess.WHITE)) * value
        score -= len(board.pieces(piece_type, chess.BLACK)) * value
    return score


def _fallback_best_move(board: chess.Board) -> tuple[str, str]:
    best_move = None
    best_eval = None

    for move in board.legal_moves:
        board.push(move)
        score = _material_score(board)
        perspective_score = score if board.turn == chess.BLACK else -score
        board.pop()

        if best_eval is None or perspective_score > best_eval:
            best_eval = perspective_score
            best_move = move

    if best_move is None:
        return "", "0"

    eval_cp = best_eval if best_eval is not None else 0
    return best_move.uci(), f"{eval_cp / 100:.2f}"


def analyze_position(fen: str) -> dict[str, str]:
    board = chess.Board(fen)
    engine_path = settings.STOCKFISH_PATH

    if engine_path and Path(engine_path).exists():
        try:
            with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
                info = engine.analyse(board, chess.engine.Limit(depth=12))
                pv = info.get("pv") or []
                best_move = pv[0].uci() if pv else ""
                score_obj = info.get("score")
                if score_obj:
                    pov = score_obj.pov(board.turn)
                    if pov.is_mate():
                        evaluation = f"mate {pov.mate()}"
                    else:
                        evaluation = f"{pov.score(mate_score=100000) / 100:.2f}"
                else:
                    evaluation = "0"
                return {
                    "best_move": best_move,
                    "evaluation": evaluation,
                    "source": "stockfish",
                }
        except Exception:
            pass

    best_move, evaluation = _fallback_best_move(board)
    return {
        "best_move": best_move,
        "evaluation": evaluation,
        "source": "fallback",
    }
