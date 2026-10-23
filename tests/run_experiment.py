import csv
from pathlib import Path

from app.routing import standard_rip, ripguard
from app.topology import LINKS, ROUTERS


OUTPUT_FILE = Path("results/comparison_results.csv")


def prepare_links(scenario):
    """Create an independent set of links for each scenario."""

    links = [link.copy() for link in LINKS]

    if scenario == "congestion":
        for link in links:
            if {link["source"], link["target"]} in [
                {"R1", "R2"},
                {"R2", "R3"},
            ]:
                link["latency_ms"] *= 3
                link["utilization_pct"] = min(
                    100,
                    link["utilization_pct"] + 25,
                )

    return links


def run_experiment():
    """Compare route selection under multiple scenarios."""

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    scenarios = [
        {
            "name": "normal",
            "failed_links": set(),
        },
        {
            "name": "link_failure",
            "failed_links": {
                frozenset(("R1", "R4"))
            },
        },
        {
            "name": "congestion",
            "failed_links": set(),
        },
    ]

    results = []

    for scenario in scenarios:
        scenario_name = scenario["name"]
        links = prepare_links(scenario_name)
        failed_links = scenario["failed_links"]

        for source, destination in [
            ("R1", "R6"),
            ("R2", "R6"),
            ("R1", "R3"),
        ]:
            standard = standard_rip(
                source,
                destination,
                failed_links=failed_links,
                links=links,
            )

            improved = ripguard(
                source,
                destination,
                failed_links=failed_links,
                links=links,
            )

            results.append({
                "scenario": scenario_name,
                "source": source,
                "destination": destination,
                "model": "Standard RIP baseline",
                "path": (
                    " -> ".join(standard["path"])
                    if standard["path"]
                    else "No route"
                ),
                "hop_count": standard["hop_count"],
                "path_cost": "",
            })

            results.append({
                "scenario": scenario_name,
                "source": source,
                "destination": destination,
                "model": "RIPGuard",
                "path": (
                    " -> ".join(improved["path"])
                    if improved["path"]
                    else "No route"
                ),
                "hop_count": improved["hop_count"],
                "path_cost": improved["path_cost"],
            })

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:
        fieldnames = [
            "scenario",
            "source",
            "destination",
            "model",
            "path",
            "hop_count",
            "path_cost",
        ]

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(results)

    print(f"Experiment completed: {len(results)} results")
    print(f"Results saved to: {OUTPUT_FILE.resolve()}")
    print("\nSample results:")

    for row in results[:6]:
        print(row)


if __name__ == "__main__":
    run_experiment()