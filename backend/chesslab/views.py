import io
import json
import urllib.error
import urllib.request

import chess
import chess.pgn
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AnalysisHistory
from .serializers import AnalyzeRequestSerializer
from .services import analyze_position


def _fetch_json(url: str) -> dict:
	request = urllib.request.Request(
		url,
		headers={"User-Agent": "ChessLearn/1.0"},
	)
	with urllib.request.urlopen(request, timeout=10) as response:
		return json.loads(response.read().decode("utf-8"))


def _final_fen_from_pgn(pgn_text: str) -> str:
	game = chess.pgn.read_game(io.StringIO(pgn_text))
	if not game:
		return ""
	board = game.board()
	for move in game.mainline_moves():
		board.push(move)
	return board.fen()


def _result_label(game_data: dict, username: str) -> str:
	if not username:
		return ""
	username = username.lower()
	white = game_data.get("white", {})
	black = game_data.get("black", {})
	white_user = str(white.get("username", "")).lower()
	black_user = str(black.get("username", "")).lower()
	player_side = "white" if white_user == username else "black" if black_user == username else ""

	result = ""
	if player_side == "white":
		result = white.get("result", "")
	elif player_side == "black":
		result = black.get("result", "")

	win_results = {"win"}
	draw_results = {
		"stalemate",
		"agreed",
		"repetition",
		"insufficient",
		"timevsinsufficient",
		"50move",
	}
	if result in win_results:
		return "Win"
	if result in draw_results:
		return "Draw"
	if result:
		return "Loss"
	return ""


@login_required
def analyzer_view(request: HttpRequest) -> HttpResponse:
	fen = chess.STARTING_FEN
	result = None

	if request.method == "POST":
		fen = request.POST.get("fen", "").strip() or chess.STARTING_FEN
		serializer = AnalyzeRequestSerializer(data={"fen": fen})
		if serializer.is_valid():
			fen = serializer.validated_data["fen"]
			result = analyze_position(fen)
			AnalysisHistory.objects.create(
				user=request.user,
				fen=fen,
				best_move=result["best_move"],
				evaluation=result["evaluation"],
				source=result["source"],
			)
		else:
			messages.error(request, "Please provide a valid FEN string.")

	history = AnalysisHistory.objects.filter(user=request.user)[:10]
	return render(
		request,
		"chesslab/analyzer.html",
		{
			"fen": fen,
			"result": result,
			"history": history,
		},
	)


def play_view(request: HttpRequest) -> HttpResponse:
	return render(request, "chesslab/play.html")


@login_required
def import_games_view(request: HttpRequest) -> HttpResponse:
	linked_username = (request.user.chess_com_username or "").strip()
	username = linked_username
	games = []

	if request.method == "POST":
		username = (request.POST.get("username") or "").strip() or linked_username
		if not username:
			messages.error(request, "Add your Chess.com username to import games.")
		else:
			if username and username != linked_username:
				request.user.chess_com_username = username
				request.user.save(update_fields=["chess_com_username"])
				linked_username = username
			try:
				archives_payload = _fetch_json(
					f"https://api.chess.com/pub/player/{username}/games/archives"
				)
				archives = archives_payload.get("archives", [])
				if not archives:
					messages.warning(request, "No game archives found for this username.")
				else:
					latest_archive = archives[-1]
					games_payload = _fetch_json(latest_archive)
					raw_games = games_payload.get("games", [])
					sorted_games = sorted(raw_games, key=lambda item: item.get("end_time", 0), reverse=True)
					for game_data in sorted_games[:5]:
						pgn_text = game_data.get("pgn", "")
						final_fen = _final_fen_from_pgn(pgn_text) if pgn_text else ""
						analysis = analyze_position(final_fen) if final_fen else {"best_move": "", "evaluation": ""}
						games.append(
							{
								"white": game_data.get("white", {}).get("username", ""),
								"black": game_data.get("black", {}).get("username", ""),
								"url": game_data.get("url", ""),
								"time_control": game_data.get("time_control", ""),
								"result": _result_label(game_data, username),
								"final_fen": final_fen,
								"analysis": analysis,
							}
						)
					if not games:
						messages.info(request, "No games were found in the latest archive.")
			except (urllib.error.URLError, json.JSONDecodeError, TimeoutError):
				messages.error(request, "Unable to reach Chess.com right now. Try again later.")

	return render(
		request,
		"chesslab/import_games.html",
		{
			"username": username,
			"linked_username": linked_username,
			"games": games,
		},
	)


class AnalyzePositionApiView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		serializer = AnalyzeRequestSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		fen = serializer.validated_data["fen"]

		result = analyze_position(fen)
		AnalysisHistory.objects.create(
			user=request.user,
			fen=fen,
			best_move=result["best_move"],
			evaluation=result["evaluation"],
			source=result["source"],
		)
		return Response(result, status=status.HTTP_200_OK)
