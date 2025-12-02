# tests/test_simulation.py
import pytest
from egoists_sim.backend.simulation import simulate, create_players, run_pairwise_tournament

def test_create_players_counts():
    players = create_players(10, 30.0)
    assert len(players) == 10
    num_altruists = sum(1 for p in players if p["type"] == "altruist")
    # 30% of 10 -> int(10 * 0.3) == 3
    assert num_altruists == 3

def test_run_basic_preset():
    # Use the top-level simulate wrapper with BASIC preset
    result = simulate(4, 50.0, {"preset": "BASIC"})
    # With 4 players and 50% altruists -> 2 altruists, 2 egoists
    assert "altruists_mean" in result
    assert "egoists_mean" in result
    # numeric sanity check
    assert isinstance(result["altruists_mean"], float)
    assert isinstance(result["egoists_mean"], float)

def test_custom_matrix():
    # custom matrix where C vs C yields 10 for both and others zero
    custom = {
        "C": {"C": (10, 10), "D": (0, 0)},
        "D": {"C": (0, 0), "D": (0, 0)}
    }
    res = simulate(3, 100.0, {"matrix": custom})
    # all players are altruists so egoist mean should be 0
    assert res["info"]["num_egoists"] == 0
    assert res["egoists_mean"] == 0.0
    # altruists_mean should be > 0
    assert res["altruists_mean"] > 0.0
