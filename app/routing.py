from app.topology import ROUTERS, LINKS


def build_graph(links, failed_links=None, weighted=False):
    """Build a graph, optionally excluding failed links."""

    failed_links = failed_links or set()
    graph = {router: [] for router in ROUTERS}

    for link in links:
        a = link["source"]
        b = link["target"]

        if frozenset((a, b)) in failed_links:
            continue

        if weighted:
            cost = link_cost(link)
        else:
            cost = 1

        graph[a].append((b, cost))
        graph[b].append((a, cost))

    return graph


def link_cost(link):
    """Calculate RIPGuard's experimental weighted link cost."""

    latency = link["latency_ms"]
    loss = link["packet_loss_pct"]
    utilization = link["utilization_pct"]

    return 1 + latency / 25 + 1.5 * loss + 2 * utilization / 100


def find_path(graph, source, destination):
    """Find a minimum-cost path using Dijkstra's algorithm."""

    distances = {router: float("inf") for router in graph}
    previous = {router: None for router in graph}
    unvisited = set(graph)

    distances[source] = 0

    while unvisited:
        current = min(unvisited, key=lambda r: distances[r])

        if distances[current] == float("inf"):
            break

        if current == destination:
            break

        unvisited.remove(current)

        for neighbor, cost in graph[current]:
            if neighbor not in unvisited:
                continue

            candidate = distances[current] + cost

            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = current

    if distances[destination] == float("inf"):
        return None, None

    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return path, distances[destination]


def standard_rip(source, destination, failed_links=None, links=None):
    """Simplified RIP baseline: minimum-hop route selection."""

    links = LINKS if links is None else links

    graph = build_graph(
        links,
        failed_links=failed_links,
        weighted=False,
    )

    path, hops = find_path(graph, source, destination)

    return {
        "model": "Standard RIP baseline",
        "path": path,
        "hop_count": len(path) - 1 if path else None,
    }


def ripguard(source, destination, failed_links=None, links=None):
    """RIPGuard: minimum weighted-cost route selection."""

    links = LINKS if links is None else links

    graph = build_graph(
        links,
        failed_links=failed_links,
        weighted=True,
    )

    path, cost = find_path(graph, source, destination)

    return {
        "model": "RIPGuard",
        "path": path,
        "path_cost": round(cost, 3) if cost is not None else None,
        "hop_count": len(path) - 1 if path else None,
    }