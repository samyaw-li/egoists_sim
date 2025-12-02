import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# Simulation logic (copied from your v2)
# -------------------------------
def simulate_game(num_players, altruist_pct, payoffs):
    num_altruists = int(num_players * altruist_pct / 100)
    num_egoists = num_players - num_altruists

    altruist_payoffs = []
    egoist_payoffs = []

    for _ in range(num_players // 2):  # each player plays one pair game
        a = random.choice(['A', 'E'])
        b = random.choice(['A', 'E'])
        payoff_a, payoff_b = payoffs[(a, b)]

        if a == 'A':
            altruist_payoffs.append(payoff_a)
        else:
            egoist_payoffs.append(payoff_a)

        if b == 'A':
            altruist_payoffs.append(payoff_b)
        else:
            egoist_payoffs.append(payoff_b)

    avg_altruist = sum(altruist_payoffs) / len(altruist_payoffs)
    avg_egoist = sum(egoist_payoffs) / len(egoist_payoffs)
    return avg_altruist, avg_egoist


# -------------------------------
# UI Logic
# -------------------------------

st.title("🎮 Altruists vs Egoists Simulation")
st.write("Explore payoff dynamics between altruists and egoists under different social conditions.")

# Sidebar inputs
st.sidebar.header("Simulation Settings")
num_players = st.sidebar.slider("Total number of players", 4, 50, 20, step=2)
altruist_pct = st.sidebar.slider("Percentage of altruists (%)", 0, 100, 50)

# Game selection
st.sidebar.header("Select Game Type")
game_choice = st.sidebar.selectbox(
    "Choose a game type:",
    ["BASIC", "EYES", "PUNISH", "Custom"]
)

# Predefined payoff matrices
default_games = {
    "BASIC": {('A', 'A'): (30, 30), ('A', 'E'): (10, 50), ('E', 'A'): (50, 10), ('E', 'E'): (40, 40)},
    "EYES": {('A', 'A'): (35, 35), ('A', 'E'): (20, 50), ('E', 'A'): (50, 20), ('E', 'E'): (40, 40)},
    "PUNISH": {('A', 'A'): (25, 25), ('A', 'E'): (5, 50), ('E', 'A'): (50, 5), ('E', 'E'): (40, 40)},
}

if game_choice != "Custom":
    payoffs = default_games[game_choice]
else:
    st.sidebar.markdown("### Enter Custom Payoffs")
    AA = st.sidebar.number_input("Payoff (A vs A)", 0, 100, 30)
    AE_a = st.sidebar.number_input("Payoff (A vs E) - Altruist", 0, 100, 10)
    AE_e = st.sidebar.number_input("Payoff (A vs E) - Egoist", 0, 100, 50)
    EE = st.sidebar.number_input("Payoff (E vs E)", 0, 100, 40)
    payoffs = {
        ('A', 'A'): (AA, AA),
        ('A', 'E'): (AE_a, AE_e),
        ('E', 'A'): (AE_e, AE_a),
        ('E', 'E'): (EE, EE)
    }

# Run simulation
if st.button("▶️ Run Simulation"):
    avg_A, avg_E = simulate_game(num_players, altruist_pct, payoffs)
    st.subheader("Results")
    st.write(f"**Altruists' average payoff:** {avg_A:.2f}")
    st.write(f"**Egoists' average payoff:** {avg_E:.2f}")

    # --- Matplotlib version of the plot ---
    fig, ax = plt.subplots()
    ax.bar(["Altruists", "Egoists"], [avg_A, avg_E], color=["#333333", "#aaaaaa"])
    ax.set_title("Average Payoffs per Group")
    ax.set_ylabel("Average Payoff")
    st.pyplot(fig)