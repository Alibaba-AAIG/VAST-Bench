"""Helpers for comparing and presenting model metrics."""

from operator import itemgetter


def leaderboard(scores):
    """``scores``: iterable of ``(id, val_accuracy)``. Returns it sorted best-first."""
    return sorted(scores, key=itemgetter(1), reverse=True)


def winner(board):
    """Id of the top-ranked submission, or ``None`` if the board is empty."""
    return board[0][0] if board else None


def format_leaderboard(board) -> str:
    return "\n".join(
        f"{rank:>2}. {mid:<12} {acc:.4f}" for rank, (mid, acc) in enumerate(board, 1)
    )
