# simulation.py
import pandas as pd
import matplotlib.pyplot as plt

# --- Step 1: Load the data ---
df = pd.read_csv('egoists_altruists_by_game.csv')

# --- Step 2: Compute cumulative sums ---
df['Egoist_sum'] = df['Egoist_mean'].cumsum()
df['Altruist_sum'] = df['Altruist_mean'].cumsum()

# Ask the user what kind of data to visualize
choice = input("Type 'mean' to plot average scores or 'cumulative' to plot running totals: ").strip().lower()

plt.figure(figsize=(10, 6))

if choice == 'mean':
    plt.plot(df['Game'], df['Egoist_mean'], label='Egoists (mean)', marker='o')
    plt.plot(df['Game'], df['Altruist_mean'], label='Altruists (mean)', marker='s')
    plt.title("Average Mean Scores: Egoists vs. Altruists")
    plt.ylabel("Mean Score")

elif choice == 'cumulative':
    plt.plot(df['Game'], df['Egoist_sum'], label='Egoists (cumulative)', marker='o')
    plt.plot(df['Game'], df['Altruist_sum'], label='Altruists (cumulative)', marker='s')
    plt.title("Cumulative Mean Scores: Egoists vs. Altruists")
    plt.ylabel("Cumulative Total")

else:
    print("Invalid choice — please type 'mean' or 'cumulative'.")
    exit()

plt.xlabel("Game")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
