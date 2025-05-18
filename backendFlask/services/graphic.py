import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend for matplotlib

import matplotlib.pyplot as plt

def plot_total_production_by_state(enriched_data, save_path="total_production_by_state.png"):
    """Draw a bar chart of total production for each state and save to file."""
    states = [entry["state"] for entry in enriched_data if entry.get("total_production") is not None]
    total_productions = [entry["total_production"] for entry in enriched_data if entry.get("total_production") is not None]
    plt.figure(figsize=(12, 8))
    plt.bar(states, total_productions, color='skyblue')
    plt.xlabel("State")
    plt.ylabel("Total Production")
    plt.title("Total Production by State")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(save_path)
    plt.close()