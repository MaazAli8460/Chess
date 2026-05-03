import chess
from django.test import TestCase
from django.urls import reverse

from users.models import User


class ChessAnalyzerTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="analyzer-user", password="pass12345")

	def test_api_requires_login(self):
		response = self.client.post(reverse("chesslab:api-analyze"), {"fen": chess.STARTING_FEN})
		self.assertEqual(response.status_code, 403)

	def test_api_returns_result_for_authenticated_user(self):
		self.client.force_login(self.user)
		response = self.client.post(reverse("chesslab:api-analyze"), {"fen": chess.STARTING_FEN})
		self.assertEqual(response.status_code, 200)
		self.assertIn("best_move", response.json())
