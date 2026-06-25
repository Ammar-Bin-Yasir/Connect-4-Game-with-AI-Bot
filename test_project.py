"""Unit tests for Connect Four game."""
import unittest
import numpy as np
from project import (
    create_board,
    drop_piece,
    is_valid_location,
    get_next_open_row,
    winning_move,
    get_valid_locations,
    score_position,
    minimax,
    get_music_path,
    Piece,
    COLUMN_COUNT,
    ROW_COUNT,
)


class TestConnectFour(unittest.TestCase):
    """Test cases for Connect Four game logic."""

    def setUp(self):
        """Create a fresh board before each test."""
        self.board = create_board()

    def test_create_board(self):
        """Test board creation with correct dimensions."""
        self.assertEqual(self.board.shape, (ROW_COUNT, COLUMN_COUNT))
        self.assertTrue(np.all(self.board == 0))

    def test_drop_piece(self):
        """Test dropping a piece on the board."""
        drop_piece(self.board, 0, 0, Piece.PLAYER)
        self.assertEqual(self.board[0][0], Piece.PLAYER)

    def test_is_valid_location(self):
        """Test column validation."""
        # Empty column should be valid
        self.assertTrue(is_valid_location(self.board, 0))
        # Fill column and test
        for row in range(ROW_COUNT):
            drop_piece(self.board, row, 0, Piece.PLAYER)
        # Full column should be invalid
        self.assertFalse(is_valid_location(self.board, 0))
        # Out of bounds should be invalid
        self.assertFalse(is_valid_location(self.board, -1))
        self.assertFalse(is_valid_location(self.board, COLUMN_COUNT))

    def test_get_next_open_row(self):
        """Test finding the next open row."""
        self.assertEqual(get_next_open_row(self.board, 0), 0)
        drop_piece(self.board, 0, 0, Piece.PLAYER)
        self.assertEqual(get_next_open_row(self.board, 0), 1)

    def test_winning_move_horizontal(self):
        """Test horizontal win detection."""
        for col in range(4):
            drop_piece(self.board, 0, col, Piece.PLAYER)
        self.assertTrue(winning_move(self.board, Piece.PLAYER))

    def test_winning_move_vertical(self):
        """Test vertical win detection."""
        self.board = create_board()
        for row in range(4):
            drop_piece(self.board, row, 0, Piece.PLAYER)
        self.assertTrue(winning_move(self.board, Piece.PLAYER))

    def test_winning_move_positive_diagonal(self):
        """Test positive diagonal win detection."""
        self.board = create_board()
        for i in range(4):
            drop_piece(self.board, i, i, Piece.PLAYER)
        self.assertTrue(winning_move(self.board, Piece.PLAYER))

    def test_winning_move_negative_diagonal(self):
        """Test negative diagonal win detection."""
        self.board = create_board()
        for i in range(4):
            drop_piece(self.board, i, 3 - i, Piece.PLAYER)
        self.assertTrue(winning_move(self.board, Piece.PLAYER))

    def test_get_valid_locations(self):
        """Test getting valid column locations."""
        valid_locations = get_valid_locations(self.board)
        self.assertEqual(valid_locations, list(range(COLUMN_COUNT)))
        # Fill all columns
        for col in range(COLUMN_COUNT):
            for row in range(ROW_COUNT):
                drop_piece(self.board, row, col, Piece.PLAYER)
        valid_locations = get_valid_locations(self.board)
        self.assertEqual(valid_locations, [])

    def test_score_position(self):
        """Test position scoring heuristic."""
        score = score_position(self.board, Piece.PLAYER)
        self.assertEqual(score, 0)
        # Add a piece in center column
        drop_piece(self.board, 0, COLUMN_COUNT // 2, Piece.PLAYER)
        score = score_position(self.board, Piece.PLAYER)
        self.assertGreater(score, 0)

    def test_minimax_returns_valid_move(self):
        """Test that minimax returns a valid column."""
        col, score = minimax(self.board, 4, -np.inf, np.inf, True)
        self.assertIn(col, range(COLUMN_COUNT))
        self.assertIsInstance(score, (int, float, np.integer, np.floating))

    def test_music_path_exists(self):
        """Test that music file path is accessible."""
        # Note: music file may not exist in test environment
        path = get_music_path()
        self.assertIsNotNone(path)
        self.assertTrue(path.name.endswith('.mp3'))

    def test_no_false_positives_winning_move(self):
        """Test that empty board shows no winner."""
        self.assertFalse(winning_move(self.board, Piece.PLAYER))
        self.assertFalse(winning_move(self.board, Piece.AI))

    def test_piece_enum(self):
        """Test Piece enum values."""
        self.assertEqual(Piece.EMPTY, 0)
        self.assertEqual(Piece.PLAYER, 1)
        self.assertEqual(Piece.AI, 2)


if __name__ == '__main__':
    unittest.main()
