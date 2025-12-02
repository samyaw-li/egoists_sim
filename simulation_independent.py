# simulation_v2.py
import itertools
import pandas as pd
import matplotlib.pyplot as plt

# --- Step 1: Basic setup ---
NUM_PLAYERS = int(input("Enter total number of players (e.g., 16): ") or 16)
altruist_ratio = float(input("Enter % of altruists (0-100, e.g., 50): ") or 50) / 100

players = []
num_altruists = int(NUM_PLAYERS * altruist_ratio)

for i in range(NUM_PLAYERS):
    if i < num_altruists:
        players.append({"id": i, "type": "altruist", "action": "C"})
    else:
        players.append({"id": i, "type": "egoist", "action": "D"})

# --- Step 2: Define payoff matrices for multiple games ---
game_matrices = {
    "BASIC": {
        "C": {"C": (3, 3), "D": (0, 5)},
        "D": {"C": (5, 0), "D": (1, 1)}
    },
    "EYES": {  # being watched encourages cooperation
        "C": {"C": (3.5, 3.5), "D": (0, 4.5)},
        "D": {"C": (4.5, 0), "D": (1, 1)}
    },
    "PUNISH": {  # defectors get penalized
        "C": {"C": (3, 3), "D": (-1, 5)},
        "D": {"C": (5, -1), "D": (0, 0)}
    }
}

def create_custom_game():
    print("\n--- Custom Game Creator ---")
    print("You’ll enter payoffs for each interaction type (format: a,b for Player1, Player2).")
    
    def get_pair(prompt):
        while True:
            try:
                vals = input(prompt).strip().split(",")
                if len(vals) != 2:
                    raise ValueError
                return (float(vals[0]), float(vals[1]))
            except ValueError:
                print("Please enter two numbers separated by a comma, like 3,3 or 0,5.")
    
    # Define payoffs for the 4 possible action pairs
    CC = get_pair("Payoff for C vs C: ")
    CD = get_pair("Payoff for C vs D: ")
    DC = get_pair("Payoff for D vs C: ")
    DD = get_pair("Payoff for D vs D: ")

    return {
        "C": {"C": CC, "D": CD},
        "D": {"C": DC, "D": DD}
    }

# --- Step 3: Function to simulate a single game type ---
def simulate_game(game_name, payoff_matrix):
    results = {p["id"]: 0 for p in players}
    for i, j in itertools.combinations(range(NUM_PLAYERS), 2):
        p1, p2 = players[i], players[j]
        a1, a2 = p1["action"], p2["action"]
        payoff1, payoff2 = payoff_matrix[a1][a2]
        results[p1["id"]] += payoff1
        results[p2["id"]] += payoff2

    altruist_scores = [results[p["id"]] for p in players if p["type"] == "altruist"]
    egoist_scores = [results[p["id"]] for p in players if p["type"] == "egoist"]
    altruist_mean = sum(altruist_scores) / len(altruist_scores)
    egoist_mean = sum(egoist_scores) / len(egoist_scores)
    return altruist_mean, egoist_mean

# --- Step 4: Interactive game selection and play loop ---

results = []
print("\nWelcome to the Public Goods Game Simulation!")
print("You’ll choose a game each round — either a preset or a custom payoff matrix.\n")

while True:
    print("\nAvailable games:")
    for g in game_matrices.keys():
        print(f" - {g}")
    print(" - CUSTOM (define your own payoff matrix)")
    print(" - QUIT (end simulation and show results)")

    choice = input("\nSelect a game type: ").strip().upper()

    if choice == "QUIT":
        break
    elif choice == "CUSTOM":
        matrix = create_custom_game()
        game_name = "CUSTOM"
    elif choice in game_matrices:
        matrix = game_matrices[choice]
        game_name = choice
    else:
        print("Invalid choice. Please try again.")
        continue

    # Run the selected game
    a_mean, e_mean = simulate_game(game_name, matrix)
    results.append({
        "Round": len(results) + 1,
        "Game": game_name,
        "Altruists": a_mean,
        "Egoists": e_mean
    })

    print(f"\nRound result — {game_name}")
    print(f"Altruists: {a_mean:.2f} | Egoists: {e_mean:.2f}")

    cont = input("\nPlay another round? (y/n): ").strip().lower()
    if cont != "y":
        break

# --- Step 5: Plot results ---
df = pd.DataFrame(results)
df = pd.DataFrame(results)
df["Altruists_cumulative_total"] = df["Altruists"].cumsum()
df["Egoists_cumulative_total"] = df["Egoists"].cumsum()

plt.figure(figsize=(10, 6))
plt.plot(df["Round"], df["Egoists_cumulative_total"], label="Egoists (Cumulative Total)", marker="o", linestyle="--", color="gray")
plt.plot(df["Round"], df["Altruists_cumulative_total"], label="Altruists (Cumulative Total)", marker="s", linestyle="-", color="black")
plt.title("Cumulative Payoffs Over Rounds")
plt.xlabel("Round Number")
plt.ylabel("Cumulative Average Payoff")
plt.xticks(df["Round"])
plt.legend()
plt.tight_layout()
plt.show()