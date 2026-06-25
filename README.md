# Connect 4 — Player vs AI

A Connect 4 game built in Python with Pygame, where you play against an AI opponent powered by the **minimax algorithm with alpha-beta pruning**.

https://github.com/user-attachments/assets/9dbab827-e713-4d99-9c34-1055dade781a
<!-- Record a short gameplay clip and drop it here as demo.gif — this matters more than any paragraph of text. -->

## What this project demonstrates

This started as a CS50P final project, but the AI engine is the real centerpiece: a from-scratch implementation of game-tree search with a hand-tuned positional evaluation function — not a library call.

- **Minimax with alpha-beta pruning** — searches the game tree to a fixed depth, pruning branches that can't affect the final decision
- **Custom heuristic evaluation** — scores non-terminal board states by weighting center-column control, open three/two-in-a-rows, and blocking the opponent's threats
- **Clean game-state representation** using NumPy arrays and an `IntEnum` for piece types
- **Test coverage** for core game logic (`test_project.py`)

## How the AI works

When it's the AI's turn, it doesn't just pick a winning move if one exists — it looks several moves ahead by simulating both players' best play:

1. **Minimax** builds a tree of possible future board states. The AI (maximizing player) tries to pick moves that lead to the best outcome *assuming the opponent always plays optimally against it* (minimizing player).
2. Since a full Connect 4 game tree is far too large to search completely, the search is cut off at a fixed depth (`AI_DIFFICULTY = 4` moves ahead). At that depth, instead of knowing the actual outcome, the AI estimates how good a position is using `score_position()`.
3. **Alpha-beta pruning** is the optimization that makes this fast enough to run in real time: if the AI already knows the opponent has a better response available elsewhere in the tree, it stops exploring a branch early instead of fully evaluating it. This doesn't change the final decision — it just skips work that can't change the outcome.
4. The evaluation function (`evaluate_window` + `score_position`) scores the board by sliding a 4-cell "window" across every row, column, and diagonal, rewarding the AI's own three-in-a-rows and open two-in-a-rows, while penalizing the opponent's near-wins.

## Tech stack

- **Python 3**
- **Pygame** — rendering, input handling, sound
- **NumPy** — board state representation

## Running it locally

```bash
git clone https://github.com/Ammar-Bin-Yasir/Connect-4-Game-with-AI-Bot.git
cd Connect-4-Game-with-AI-Bot
pip install -r requirements.txt
python project.py
```

Click any column to drop your piece (red). The AI (yellow) responds automatically.

## Project structure

```
project.py          # game loop, board logic, rendering, and AI engine
test_project.py      # unit tests for core game logic
requirements.txt      # dependencies (pygame, numpy)
Sound Effects/        # background music
```

## Known limitations / future improvements

- AI search depth is fixed at 4 — could be made adaptive (deeper in the endgame, when fewer columns remain) for stronger play without a runtime cost increase
- No difficulty selector — could expose `AI_DIFFICULTY` as a menu option (easy/medium/hard)
- No move undo or game replay/history log
- Win detection and evaluation both re-scan the whole board each call — could be optimized to update incrementally as pieces are placed, rather than recomputing from scratch every turn

## Background

Originally built as a final project for [CS50's Introduction to Programming with Python](https://cs50.harvard.edu/python/).
