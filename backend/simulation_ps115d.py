import random

# --- PLAYER CREATION --------------------------------------------------------

def create_players_ps115d(num_players, altruist_ratio, halfway_ratio=0.0):
    """
    Create players of 3 types:
    - altruist: gives 10 (keeps 0)
    - halfway: gives 5 (keeps 5)
    - egoist: gives 0 (keeps 10)
    """
    players = []
    num_altruists = int(num_players * altruist_ratio)
    num_halfway = int(num_players * halfway_ratio)
    num_egoists = num_players - num_altruists - num_halfway

    # Build type list
    types = (
        ["altruist"] * num_altruists +
        ["halfway"] * num_halfway +
        ["egoist"] * num_egoists
    )
    random.shuffle(types)

    for i, t in enumerate(types):
        if t == "altruist":
            choice = 10
        elif t == "halfway":
            choice = 5
        else:
            choice = 0

        players.append({
            "id": i,
            "type": t,
            "choice": choice
        })

    return players


# --- BASIC PUBLIC GOODS GAME ------------------------------------------------

def simulate_basic(players):
    """Simulate BASIC PS115D public goods game."""
    n = len(players)
    results = {}

    for p in players:
        # Build group of size 10: p + 9 random others
        others = random.sample([x for x in players if x["id"] != p["id"]], 9)
        group = [p] + others

        pot = sum(member["choice"] for member in group) * 5
        keep = 10 - p["choice"]

        results[p["id"]] = keep + pot / 10

    return results


# --- COMPETITIVE PUBLIC GOODS GAME -----------------------------------------

def simulate_competitive(players):
    """Simulate COMPETITIVE PS115D game with round-robin groups."""
    n = len(players)
    groups = []
    results = {}

    # Precompute groups of size 10
    for i in range(n):
        group = [players[(i + k) % n] for k in range(10)]
        pot = sum(m["choice"] for m in group) * 5
        groups.append((group, pot))

    # Pay each player
    for i, p in enumerate(players):
        group_i, pot_i = groups[i]
        group_j, pot_j = groups[(i + 1) % n]

        keep = 10 - p["choice"]

        if pot_i > pot_j:
            payoff = keep + (pot_i / 10) + (pot_j / 10)
        else:
            payoff = keep

        results[p["id"]] = payoff

    return results


# --- EVOLUTION MECHANISM ----------------------------------------------------

def evolve(players, results):
    """Players die w/ probability and are replaced by opposite."""
    for p in players:
        payoff = results[p["id"]]
        survival_prob = payoff / 55  # normalize to [0,1]

        if random.random() > survival_prob:
            # death → replacement
            if p["type"] == "altruist":
                p["type"] = "egoist"
                p["choice"] = 0

            elif p["type"] == "egoist":
                p["type"] = "altruist"
                p["choice"] = 10

            else:  # halfway house
                if random.random() < 0.5:
                    p["type"] = "altruist"
                    p["choice"] = 10
                else:
                    p["type"] = "egoist"
                    p["choice"] = 0

    return players


# --- MAIN SIMULATION STEP ---------------------------------------------------

def run_ps115d_round(players, game_type):
    """Runs one full PS115D evolutionary step."""
    if game_type == "BASIC":
        results = simulate_basic(players)
    elif game_type == "COMPETITIVE":
        results = simulate_competitive(players)
    else:
        raise ValueError("Invalid PS115D game type")

    evolved = evolve(players, results)

    # Statistics
    altruist_mean = sum(results[p["id"]] for p in evolved if p["type"] == "altruist")
    egoist_mean = sum(results[p["id"]] for p in evolved if p["type"] == "egoist")
    halfway_mean = sum(results[p["id"]] for p in evolved if p["type"] == "halfway")

    # Avoid div0
    numA = len([p for p in evolved if p["type"] == "altruist"])
    numE = len([p for p in evolved if p["type"] == "egoist"])
    numH = len([p for p in evolved if p["type"] == "halfway"])

    return {
        "results": results,
        "players": evolved,
        "altruist_mean": altruist_mean / numA if numA else 0,
        "egoist_mean": egoist_mean / numE if numE else 0,
        "halfway_mean": halfway_mean / numH if numH else 0,
    }
