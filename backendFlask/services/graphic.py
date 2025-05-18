import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg') # Use a non-GUI backend for matplotlib (hopefully won't explode like earlier)

def plot_total_production_by_state(enriched_data, save_path="total_production_by_state.png"):
    """
    Draws a bar chart of total production for each state.
    Saves the plot to a file.
    """
    states = []
    total_productions = []

    for entry in enriched_data:
        if entry.get("total_production") is not None:
            states.append(entry["state"])
            total_productions.append(entry["total_production"])

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