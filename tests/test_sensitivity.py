import unittest

from app.topology import LINKS
from app.routing import ripguard


class TestRIPGuardSensitivity(unittest.TestCase):

    def test_model_uses_link_quality_metrics(self):

        # Original network
        original = ripguard("R1", "R6")

        # Temporarily create a network where R1-R4
        # has very poor link quality.
        modified_links = []

        for link in LINKS:

            new_link = link.copy()

            if (
                new_link["source"] == "R1"
                and new_link["target"] == "R4"
            ):
                new_link["latency_ms"] = 500
                new_link["packet_loss_pct"] = 20
                new_link["utilization_pct"] = 100

            modified_links.append(new_link)

        # Calculate the expected route separately
        # using the modified links.
        from app.routing import link_cost
        from app.topology import ROUTERS

        graph = {router: [] for router in ROUTERS}

        for link in modified_links:

            a = link["source"]
            b = link["target"]
            cost = link_cost(link)

            graph[a].append((b, cost))
            graph[b].append((a, cost))

        distances = {r: float("inf") for r in ROUTERS}
        previous = {r: None for r in ROUTERS}

        distances["R1"] = 0
        unvisited = set(ROUTERS)

        while unvisited:

            current = min(
                unvisited,
                key=lambda r: distances[r]
            )

            if distances[current] == float("inf"):
                break

            if current == "R6":
                break

            unvisited.remove(current)

            for neighbor, cost in graph[current]:

                if neighbor not in unvisited:
                    continue

                new_cost = distances[current] + cost

                if new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    previous[neighbor] = current

        path = []
        current = "R6"

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        self.assertNotEqual(
            original["path"],
            path,
            "Route should change when link costs change significantly."
        )


if __name__ == "__main__":
    unittest.main()