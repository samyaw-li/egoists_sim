import random

# --------------------------------------------------------------------
# TYPE MAPPING
# --------------------------------------------------------------------
# keep 10 → give 0  → Egoist
# keep 5  → give 5  → Halfway House
# keep 0  → give 10 → Altruist

TYPE_TO_GIVE = {
    "egoist": 0,
    "halfway": 5,
    "altruist": 10,
}

TYPE_LIST = ["altruist", "halfway", "egoist"]

# Payoffs range is [0, 55]
MAX_PAYOFF = 55

# --------------------------------------------------------------------
# Create population (120 players by default)
# --------------------------------------------------------------------
def create_population(n=120, ratios=None):
    """
    ratios = dict(altruist=?, halfway=?, egoist=?)
    """
    if ratios is None:
        ratios = {"altruist": 0.33, "halfway": 0.34, "egoist": 0.33}

    population = []
    counts = {t: int(ratios[t] * n) for t in TYPE_LIST}

    # Fix rounding errors
    while sum(counts.values()) < n:
        counts["egoist"] += 1

    pid = 0
    for t in TYPE_LIST:
        for _ in range(counts[t]):
            population.append({
                "id": pid,
                "type": t,
                "payoff": 0,
            })
            pid += 1

    random.shuffle(population)
    return population

# --------------------------------------------------------------------
# BASIC GAME: payoff calculation
# --------------------------------------------------------------------
def compute_basic_payoff(group, target_player):
    """
    group: list of 10 players including target_player
    Returns payoff for target_player under BASIC rules.
    """
    give_amount = TYPE_TO_GIVE[target_player["type"]]
    keep_amount = 10 - give_amount

    total_contributions = sum(TYPE_TO_GIVE[p["type"]] for p in group)
    pot = total_contributions * 5
    share = pot / 10

    return keep_amount + share

# --------------------------------------------------------------------
# COMPETITIVE GAME: jets vs sharks
# --------------------------------------------------------------------
def compute_competitive_payoff(group_A, group_B, target_player):
    """
    group_A: player's own group (10 players)
    group_B: opponent group (10 players)
    """
    give_amount = TYPE_TO_GIVE[target_player["type"]]
    keep_amount = 10 - give_amount

    contrib_A = sum(TYPE_TO_GIVE[p["type"]] for p in group_A) * 5
    contrib_B = sum(TYPE_TO_GIVE[p["type"]] for p in group_B) * 5

    if contrib_A > contrib_B:
        # Winning group: own pot share + losing pot share
        return keep_amount + (contrib_A / 10) + (contrib_B / 10)
    else:
        # Losing group: only keep amount
        return keep_amount

# --------------------------------------------------------------------
# EVOLUTIONARY STEP
# --------------------------------------------------------------------
def evolutionary_update(population):
    """
    Players survive probabilistically based on payoff. 
    Dying players are replaced by opposite type (halfway random).
    """
    new_population = []

    for p in population:
        survival_prob = p["payoff"] / MAX_PAYOFF
        survive = random.random() < survival_prob

        if survive:
            new_population.append({**p, "payoff": 0})
        else:
            if p["type"] == "altruist":
                new_type = "egoist"
            elif p["type"] == "egoist":
                new_type = "altruist"
            else:  # halfway
                new_type = random.choice(["altruist", "egoist"])

            new_population.append({
                "id": p["id"],
                "type": new_type,
                "payoff": 0,
            })

    return new_population

# --------------------------------------------------------------------
# MAIN SIMULATION ROUND
# --------------------------------------------------------------------
def simulate_round_ps115d(population, mode="BASIC"):
    """
    mode = "BASIC" or "COMPETITIVE"
    Returns updated population + summary statistics.
    """
    n = len(population)
    for p in population:
        p["payoff"] = 0

    if mode == "BASIC":
        for i, p in enumerate(population):
            # group of 10 = p + 9 random others
            others = [x for j, x in enumerate(population) if j != i]
            group = random.sample(others, 9) + [p]
            p["payoff"] = compute_basic_payoff(group, p)

    else:  # COMPETITIVE
        for i, p in enumerate(population):
            # Own group
            others_A = [x for j, x in enumerate(population) if j != i]
            group_A = random.sample(others_A, 9) + [p]

            # Opponent group: next player round-robin
            opponent_index = (i + 1) % n
            opponent = population[opponent_index]
            others_B = [x for j, x in enumerate(population) if j != opponent_index]
            group_B = random.sample(others_B, 9) + [opponent]

            p["payoff"] = compute_competitive_payoff(group_A, group_B, p)

    # Evolutionary update
    new_pop = evolutionary_update(population)

    # Summary statistics
    counts_dict = {t: 0 for t in TYPE_LIST}
    for p in new_pop:
        counts_dict[p["type"]] += 1

    total = len(new_pop)
    summary = {
        "nC": counts_dict["altruist"],
        "nD": counts_dict["egoist"],
        "nH": counts_dict["halfway"],
        "propC": counts_dict["altruist"] / total,
        "propD": counts_dict["egoist"] / total,
        "propH": counts_dict["halfway"] / total,
    }

    return new_pop, summary

# --------------------------------------------------------------------
# Example usage
# --------------------------------------------------------------------
if __name__ == "__main__":
    pop = create_population()
    for t in range(10):
        pop, stats = simulate_round_ps115d(pop, mode="BASIC")
        print(f"Round {t+1} BASIC:", stats)

    pop = create_population()
    for t in range(10):
        pop, stats = simulate_round_ps115d(pop, mode="COMPETITIVE")
        print(f"Round {t+1} COMPETITIVE:", stats)
