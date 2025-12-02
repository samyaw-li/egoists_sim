import itertools

def create_custom_matrix(custom_payoff):
    """Convert custom payoff dict to a 2x2 payoff matrix."""
    return {
        "C": {"C": tuple(custom_payoff["CC"]), "D": tuple(custom_payoff["CD"])},
        "D": {"C": tuple(reversed(custom_payoff["CD"])), "D": tuple(custom_payoff["DD"])},
    }

def create_players(num_players=16, altruist_ratio=0.5):
    """Initialize players with altruist or egoist strategy."""
    players = []
    num_altruists = int(num_players * altruist_ratio)
    for i in range(num_players):
        p_type = "altruist" if i < num_altruists else "egoist"
        action = "C" if p_type == "altruist" else "D"
        players.append({"id": i, "type": p_type, "action": action})
    return players

game_matrices = {
    "BASIC": {"C": {"C": (3, 3), "D": (0, 5)}, "D": {"C": (5, 0), "D": (1, 1)}},
    "EYES": {"C": {"C": (3.5, 3.5), "D": (0, 4.5)}, "D": {"C": (4.5, 0), "D": (1, 1)}},
    "PUNISH": {"C": {"C": (3, 3), "D": (-1, 5)}, "D": {"C": (5, -1), "D": (0, 0)}},
}

def simulate_round(players, payoff_matrix):
    """Run one simulation round between all pairs."""
    results = {p["id"]: 0 for p in players}
    for i, j in itertools.combinations(range(len(players)), 2):
        p1, p2 = players[i], players[j]
        a1, a2 = p1["action"], p2["action"]
        payoff1, payoff2 = payoff_matrix[a1][a2]
        results[p1["id"]] += payoff1
        results[p2["id"]] += payoff2

    altruist_scores = [results[p["id"]] for p in players if p["type"] == "altruist"]
    egoist_scores = [results[p["id"]] for p in players if p["type"] == "egoist"]

    return {
        "altruist_mean": sum(altruist_scores) / len(altruist_scores),
        "egoist_mean": sum(egoist_scores) / len(egoist_scores)
    }

def run_simulation_round(num_players, altruist_ratio, game_type, custom_payoff=None, history=None):
    """Orchestrate a single round, tracking cumulative stats."""
    players = create_players(num_players, altruist_ratio)

    if game_type == "CUSTOM":
        if not custom_payoff:
            raise ValueError("Missing custom payoff data.")
        matrix = create_custom_matrix(custom_payoff)
    elif game_type in game_matrices:
        matrix = game_matrices[game_type]
    else:
        raise ValueError(f"Unknown game_type: {game_type}")

    round_result = simulate_round(players, matrix)
    round_result["game"] = game_type
    round_result["round"] = len(history) + 1 if history else 1

    history = history or []
    history.append(round_result)

    # Compute cumulative means
    cumulative_altruist = sum(r["altruist_mean"] for r in history)
    cumulative_egoist = sum(r["egoist_mean"] for r in history)
    round_result["cumulative_altruist"] = cumulative_altruist
    round_result["cumulative_egoist"] = cumulative_egoist

    return round_result, history
