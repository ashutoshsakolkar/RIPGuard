from app.routing import ripguard, link_cost
from app.topology import LINKS


class RIPGuardController:
    """
    RIPGuard routing controller.

    Features:
    1. Multi-metric route selection.
    2. Configurable route-switching threshold.
    3. Immediate failover when the active route fails.
    4. Link restoration and route reevaluation.
    5. Dynamic link-metric updates.
    6. Route-change tracking.
    """

    def __init__(self, source, destination, threshold_pct=10):
        if not 0 <= threshold_pct <= 100:
            raise ValueError(
                "Threshold must be between 0 and 100."
            )

        self.source = source
        self.destination = destination
        self.threshold_pct = threshold_pct

        self.active_path = None
        self.active_cost = None

        self.route_changes = 0
        self.failed_links = set()

        # Use a private copy so experiments do not modify topology.py.
        self.links = [link.copy() for link in LINKS]

    def _path_cost(self, path):
        """Calculate the current cost of a particular route."""

        if not path or len(path) < 2:
            return 0.0

        total_cost = 0.0

        for router_a, router_b in zip(path, path[1:]):

            link_failed = (
                frozenset((router_a, router_b))
                in self.failed_links
            )

            if link_failed:
                return None

            link = next(
                (
                    item
                    for item in self.links
                    if {
                        item["source"],
                        item["target"],
                    } == {router_a, router_b}
                ),
                None,
            )

            if link is None:
                return None

            total_cost += link_cost(link)

        return round(total_cost, 3)

    def update_route(self):
        """Evaluate the best route and decide whether to switch."""

        result = ripguard(
            self.source,
            self.destination,
            failed_links=self.failed_links,
            links=self.links,
        )

        candidate_path = result["path"]
        candidate_cost = result["path_cost"]

        # No usable route exists.
        # Preserve the last known route internally.
        if candidate_path is None:
            return {
                "status": "No route available",
                "path": None,
                "cost": None,
                "route_changed": False,
                "route_changes": self.route_changes,
            }

        # Select the first available route.
        if self.active_path is None:
            self.active_path = candidate_path
            self.active_cost = candidate_cost

            return {
                "status": "Initial route selected",
                "path": self.active_path.copy(),
                "cost": self.active_cost,
                "route_changed": True,
                "route_changes": self.route_changes,
            }

        # Calculate the current cost of the active route.
        current_active_cost = self._path_cost(self.active_path)

        # If the active route is broken, switch immediately.
        if current_active_cost is None:
            self.active_path = candidate_path
            self.active_cost = candidate_cost
            self.route_changes += 1

            return {
                "status": "Switched after link failure",
                "path": self.active_path.copy(),
                "cost": self.active_cost,
                "route_changed": True,
                "route_changes": self.route_changes,
            }

        # If the current route is already the best route,
        # update its cost and avoid an unnecessary switch.
        if candidate_path == self.active_path:
            self.active_cost = current_active_cost

            return {
                "status": "Current route retained",
                "path": self.active_path.copy(),
                "cost": self.active_cost,
                "route_changed": False,
                "route_changes": self.route_changes,
            }

        # Calculate the percentage improvement.
        improvement_pct = (
            (current_active_cost - candidate_cost)
            / current_active_cost
            * 100
            if current_active_cost > 0
            else 0
        )

        # Switch only when the improvement meets the threshold.
        if improvement_pct >= self.threshold_pct:
            self.active_path = candidate_path
            self.active_cost = candidate_cost
            self.route_changes += 1

            status = "Switched: improvement threshold reached"
            changed = True

        else:
            # Retain the active route if the improvement is too small.
            self.active_cost = current_active_cost

            status = "Kept current route for stability"
            changed = False

        return {
            "status": status,
            "path": self.active_path.copy(),
            "cost": self.active_cost,
            "route_changed": changed,
            "route_changes": self.route_changes,
        }

    def fail_link(self, router_a, router_b):
        """Simulate a link failure."""

        self.failed_links.add(
            frozenset((router_a, router_b))
        )

        return self.update_route()

    def restore_link(self, router_a, router_b):
        """Restore a link and reevaluate the available routes."""

        self.failed_links.discard(
            frozenset((router_a, router_b))
        )

        return self.update_route()

    def update_link_metrics(
        self,
        router_a,
        router_b,
        latency_ms=None,
        packet_loss_pct=None,
        utilization_pct=None,
    ):
        """Change link metrics and reevaluate the route."""

        # Validate inputs before changing any metrics.
        if latency_ms is not None and latency_ms < 0:
            raise ValueError(
                "Latency cannot be negative."
            )

        if (
            packet_loss_pct is not None
            and not 0 <= packet_loss_pct <= 100
        ):
            raise ValueError(
                "Packet loss must be between 0 and 100."
            )

        if (
            utilization_pct is not None
            and not 0 <= utilization_pct <= 100
        ):
            raise ValueError(
                "Utilization must be between 0 and 100."
            )

        # Find the requested link.
        for link in self.links:

            same_link = (
                link["source"] == router_a
                and link["target"] == router_b
            ) or (
                link["source"] == router_b
                and link["target"] == router_a
            )

            if not same_link:
                continue

            if latency_ms is not None:
                link["latency_ms"] = latency_ms

            if packet_loss_pct is not None:
                link["packet_loss_pct"] = packet_loss_pct

            if utilization_pct is not None:
                link["utilization_pct"] = utilization_pct

            return self.update_route()

        raise ValueError(
            f"Link {router_a}-{router_b} does not exist."
        )