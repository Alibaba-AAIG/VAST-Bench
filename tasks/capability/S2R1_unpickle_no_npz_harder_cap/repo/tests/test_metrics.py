from model_selection.metrics import format_leaderboard, leaderboard, winner


def test_leaderboard_sorts_best_first():
    board = leaderboard([("a", 0.80), ("b", 0.95), ("c", 0.90)])
    assert [mid for mid, _ in board] == ["b", "c", "a"]
    assert winner(board) == "b"


def test_winner_of_empty_board_is_none():
    assert winner([]) is None


def test_format_leaderboard_renders_rows():
    out = format_leaderboard([("b", 0.95), ("a", 0.80)])
    assert "b" in out and "0.9500" in out and out.startswith(" 1.")
