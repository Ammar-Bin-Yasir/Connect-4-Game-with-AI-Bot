"""
Connect Four Game - Player vs AI
Implements minimax algorithm with alpha-beta pruning for optimal AI moves.
"""
import math
import random
import sys
from pathlib import Path
from enum import IntEnum

import numpy as np
import pygame

# ============ BOARD CONFIGURATION ============
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 150
RADIUS = int(SQUARESIZE / 2 - 8)
WINDOW_LENGTH = 4

# ============ SCREEN CONFIGURATION ============
SCREEN_WIDTH = COLUMN_COUNT * SQUARESIZE
SCREEN_HEIGHT = (ROW_COUNT + 1) * SQUARESIZE
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# ============ COLORS ============
BLUE = (0, 102, 204)
BACKGROUND = (173, 216, 230)
RED = (255, 59, 48)
YELLOW = (255, 204, 0)
WHITE = (255, 255, 255)

# ============ GAME CONSTANTS ============
class Piece(IntEnum):
    """Enum for board pieces"""
    EMPTY = 0
    PLAYER = 1
    AI = 2


RED_COIN = Piece.PLAYER
YELLOW_COIN = Piece.AI
EMPTY = Piece.EMPTY

# ============ AI CONFIGURATION ============
AI_DIFFICULTY = 4
WINNING_SCORE = 100000000000000
LOSING_SCORE = -10000000000000

# ============ PYGAME CONFIGURATION ============
FONT_SIZE = 75
GAME_OVER_DELAY_MS = 3000
MUSIC_VOLUME = 0.5

# ============ AUDIO ============
_pygame_mixer_enabled = False


def get_music_path():
    """Get the absolute path to the game music file."""
    return Path(__file__).resolve().parent / "Sound Effects" / "game-music-loop-6-144641.mp3"


def _init_pygame():
    """Initialize Pygame engine and mixer."""
    global _pygame_mixer_enabled
    pygame.init()

    try:
        pygame.mixer.init()
        _pygame_mixer_enabled = True
        music_path = get_music_path()
        if music_path.exists():
            try:
                pygame.mixer.music.load(str(music_path))
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(MUSIC_VOLUME)
            except pygame.error:
                _pygame_mixer_enabled = False
    except pygame.error:
        _pygame_mixer_enabled = False


def _stop_music():
    """Safely stop the game music."""
    if _pygame_mixer_enabled:
        try:
            pygame.mixer.music.stop()
        except pygame.error:
            pass


# Initialize Pygame on module load
_init_pygame()
myfont = pygame.font.SysFont("monospace", FONT_SIZE)



def main():
    """Main game loop."""
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    # Initialize the main screen
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Connect Four - Player vs AI")

    draw_board(board, screen)
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _stop_music()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BACKGROUND, (0, 0, SCREEN_WIDTH, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BACKGROUND, (0, 0, SCREEN_WIDTH, SQUARESIZE))
                # Player turn
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    # Validate column bounds
                    if 0 <= col < COLUMN_COUNT and is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, RED_COIN)

                        if winning_move(board, RED_COIN):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            _stop_music()
                            screen.blit(label, (40, 10))
                            game_over = True

                        print_board(board)
                        draw_board(board, screen)

                        turn += 1
                        turn = turn % 2

        # AI turn
        if turn == 1 and not game_over:
            col, minimax_score = minimax(board, AI_DIFFICULTY, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, YELLOW_COIN)

                if winning_move(board, YELLOW_COIN):
                    label = myfont.render("AI wins!!", 1, YELLOW)
                    _stop_music()
                    screen.blit(label, (40, 10))
                    game_over = True

                print(f"AI plays column {col}, score: {minimax_score}")
                print_board(board)
                draw_board(board, screen)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(GAME_OVER_DELAY_MS)


# ============ BOARD OPERATIONS ============

def create_board():
    """Create an empty board."""
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)


def print_board(board):
    """Print the board state to console (flipped for bottom-up display)."""
    print(np.flip(board, 0))


def draw_board(board, screen):
    """Draw the game board on the pygame screen."""
    # Draw board grid and empty slots
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen,
                BLUE,
                (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE)
            )
            pygame.draw.circle(
                screen,
                BACKGROUND,
                (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)
                ),
                RADIUS
            )

    # Draw pieces
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == RED_COIN:
                pygame.draw.circle(
                    screen,
                    RED,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        SCREEN_HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)
                    ),
                    RADIUS
                )
            elif board[r][c] == YELLOW_COIN:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        SCREEN_HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)
                    ),
                    RADIUS
                )
    pygame.display.update()


def is_valid_location(board, col):
    """Check if a column has space for a new piece."""
    if col < 0 or col >= COLUMN_COUNT:
        return False
    return board[ROW_COUNT - 1][col] == EMPTY


def get_next_open_row(board, col):
    """Get the lowest empty row in the given column."""
    for r in range(ROW_COUNT):
        if board[r][col] == EMPTY:
            return r
    return None


def drop_piece(board, row, col, piece):
    """Place a piece at the specified position."""
    if row is not None:
        board[row][col] = piece
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True


# ============ WIN DETECTION ============

def winning_move(board, piece):
    """Check if the given piece has a winning configuration (4 in a row)."""
    # Check horizontal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (board[r][c] == piece and board[r][c + 1] == piece and
                    board[r][c + 2] == piece and board[r][c + 3] == piece):
                return True

    # Check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == piece and board[r + 1][c] == piece and
                    board[r + 2][c] == piece and board[r + 3][c] == piece):
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (board[r][c] == piece and board[r + 1][c + 1] == piece and
                    board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece):
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (board[r][c] == piece and board[r - 1][c + 1] == piece and
                    board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece):
                return True

    return False



# ============ AI ENGINE - MINIMAX WITH ALPHA-BETA PRUNING ============

def get_valid_locations(board):
    """Return a list of valid columns."""
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def is_terminal_node(board):
    """Check if the game has ended (win or draw)."""
    return (
        winning_move(board, RED_COIN) or
        winning_move(board, YELLOW_COIN) or
        len(get_valid_locations(board)) == 0
    )


def evaluate_window(window, piece):
    """Score a 4-window based on piece count."""
    score = 0
    opp_piece = YELLOW_COIN if piece == RED_COIN else RED_COIN

    # 4 in a row is winning
    if window.count(piece) == 4:
        score += 100
    # 3 in a row with empty space
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    # 2 in a row with 2 empty
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    # Opponent has 3 in a row - block it
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    """Evaluate board position for the AI."""
    score = 0

    # Score center column (more valuable positions)
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score horizontal windows
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score vertical windows
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def minimax(board, depth, alpha, beta, is_maximizing):
    """
    Minimax algorithm with alpha-beta pruning.

    Args:
        board: Game board state
        depth: Search depth remaining
        alpha: Alpha value for pruning
        beta: Beta value for pruning
        is_maximizing: True if maximizing player (AI), False if minimizing (player)

    Returns:
        Tuple of (best_column, score)
    """
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    # Terminal node or depth limit reached
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, YELLOW_COIN):
                return None, WINNING_SCORE
            elif winning_move(board, RED_COIN):
                return None, LOSING_SCORE
            else:  # Draw
                return None, 0
        else:  # Depth limit reached
            return None, score_position(board, YELLOW_COIN)

    if is_maximizing:
        max_value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, YELLOW_COIN)
            _, new_score = minimax(board_copy, depth - 1, alpha, beta, False)

            if new_score > max_value:
                max_value = new_score
                best_col = col
            alpha = max(alpha, max_value)
            if alpha >= beta:
                break
        return best_col, max_value
    else:  # Minimizing player
        min_value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, RED_COIN)
            _, new_score = minimax(board_copy, depth - 1, alpha, beta, True)

            if new_score < min_value:
                min_value = new_score
                best_col = col
            beta = min(beta, min_value)
            if alpha >= beta:
                break
        return best_col, min_value


if __name__ == "__main__":
    main()