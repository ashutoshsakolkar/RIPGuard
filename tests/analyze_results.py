import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


INPUT_FILE = Path("results/comparison_results.csv")
OUTPUT_DIR = Path("results/graphs")


def load_results():
    """Load experiment results from the CSV file."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Results file not found: {INPUT_FILE}"
        )

    with INPUT_FILE.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        return list(csv.DictReader(file))


def summarize_results(rows):
    """Summarize hop counts and calculated path costs."""

    grouped = defaultdict(list)

    for row in rows:
        key = (row["scenario"], row["model"])
        grouped[key].append(row)

    print("\nRIPGuard Experiment Summary")
    print("=" * 65)

    for (scenario, model), records in sorted(grouped.items()):
        hop_values = [
            int(row["hop_count"])
            for row in records
            if row["hop_count"]
        ]

        cost_values = [
            float(row["path_cost"])
            for row in records
            if row["path_cost"]
        ]

        average_hops = (
            sum(hop_values) / len(hop_values)
            if hop_values
            else 0
        )

        average_cost = (
            sum(cost_values) / len(cost_values)
            if cost_values
            else None
        )

        cost_text = (
            f"{average_cost:.3f}"
            if average_cost is not None
            else "Not calculated"
        )

        print(
            f"{scenario:15} | {model:23} | "
            f"Average hops: {average_hops:.2f} | "
            f"Average calculated cost: {cost_text}"
        )


def plot_average_hops(rows):
    """Compare average hop counts across scenarios."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    scenarios = ["normal", "congestion", "link_failure"]
    models = ["Standard RIP baseline", "RIPGuard"]

    averages = {model: [] for model in models}

    for scenario in scenarios:
        for model in models:
            values = [
                int(row["hop_count"])
                for row in rows
                if row["scenario"] == scenario
                and row["model"] == model
                and row["hop_count"]
            ]

            averages[model].append(
                sum(values) / len(values) if values else 0
            )

    x_positions = list(range(len(scenarios)))
    width = 0.35

    plt.figure(figsize=(9, 5))

    plt.bar(
        [x - width / 2 for x in x_positions],
        averages[models[0]],
        width,
        label=models[0],
    )

    plt.bar(
        [x + width / 2 for x in x_positions],
        averages[models[1]],
        width,
        label=models[1],
    )

    plt.xticks(x_positions, scenarios)
    plt.ylabel("Average hop count")
    plt.xlabel("Scenario")
    plt.title("Average Route Hops: Standard RIP vs RIPGuard")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()

    output_path = OUTPUT_DIR / "average_hops.png"
    plt.savefig(output_path, dpi=200)
    plt.close()

    print(f"\nSaved graph: {output_path}")


def main():
    rows = load_results()

    summarize_results(rows)
    plot_average_hops(rows)

    print("\nAnalysis completed.")


if __name__ == "__main__":
    main()