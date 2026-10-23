# RIPGuard — Reliability-Aware Routing Dashboard

RIPGuard is a networking project built around a simple question: **What if the route with the fewest hops isn't always the best route?**

This project explores that idea through an interactive dashboard representing a six-router network. It compares a standard RIP-style shortest-hop routing approach with RIPGuard, a custom routing strategy that also considers latency, packet loss, and link utilization.

You can change network conditions, simulate link failures, compare routes, and see how the routing decisions change.

## 🚀 Live Dashboard

**Live demo:** Coming soon. The dashboard needs to be deployed before a public link can be shared.

Once the application is hosted, its public URL will be added here so anyone can explore the dashboard directly from a browser.

**GitHub Repository:** [RIPGuard on GitHub](https://github.com/ashutoshsakolkar/RIPGuard)

## What Can You Do With RIPGuard?

The dashboard lets you experiment with different network conditions instead of looking at routing tables alone.

* **Explore the network:** View six routers connected through ten inter-router links.
* **Monitor link conditions:** View latency, packet loss, utilization, and calculated link costs.
* **Generate network conditions:** Change the simulated metrics and see how route selection responds.
* **Compare routing methods:** Compare the route chosen by the shortest-hop baseline with RIPGuard's weighted-cost route.
* **Simulate link failures:** Fail a connection, observe the route change, and restore the connection.
* **Demonstrate packet-loss penalties:** Trigger a controlled scenario where packet loss exceeds the configured 10% threshold.
* **Understand the calculations:** Inspect the formula used to calculate individual link costs.
* **Follow network events:** Use the event log and route summary to understand what changes when network conditions change.

## Understanding the Routing Approach

### 1. Standard RIP-Style Routing

The dashboard includes a baseline that selects a route using the fewest-hop principle associated with RIP.

For example, if one route reaches a destination in two hops and another takes three hops, the shortest-hop baseline prefers the two-hop route.

This approach provides a useful reference point for our comparison.

### 2. RIPGuard: Reliability-Aware Weighted Routing

RIPGuard considers more than the number of hops.

It calculates a cost for each active link based on its network conditions. The routing algorithm then searches for the available route with the lowest total weighted cost.

The cost model considers:

| Parameter          | Meaning                                         |
| ------------------ | ----------------------------------------------- |
| Latency (`L`)      | Link delay, measured in milliseconds            |
| Packet loss (`P`)  | Percentage of packets lost on a link            |
| Utilization (`U`)  | Percentage of the link's capacity being used    |
| SLA penalty        | An additional cost when packet loss exceeds 10% |
| Congestion penalty | An additional cost when utilization exceeds 80% |

### RIPGuard Cost Formula

The current model uses this formula:

```text
C = 1 + 0.4L + 5P + 0.05U + S(P) + G(U)

Packet-loss penalty:

S(P) = 0                    when P <= 10
       60 + 6(P - 10)       when P > 10

Congestion penalty:

G(U) = 0                    when U <= 80
       0.15(U - 80)^2       when U > 80
```

Here, `P = 12` represents 12% packet loss, and `U = 85` represents 85% link utilization.

The additional penalties make links that exceed the configured thresholds less attractive. This allows RIPGuard to choose a different route when an alternative has a lower total weighted cost.

**Note:** The thresholds and coefficients are design choices for this project. They are not universal networking standards.

### Why Use an SLA Penalty?

A link can remain operational while still providing poor service because of packet loss or congestion.

Without an additional penalty, a link that slightly exceeds the acceptable packet-loss threshold may not receive a sufficiently high cost to influence route selection.

RIPGuard therefore applies an extra penalty when packet loss exceeds 10%. It also applies a nonlinear congestion penalty when utilization exceeds 80%.

The objective is to make the routing decision more sensitive to links that violate the project's configured quality thresholds.

## RIP vs RIPGuard: What Are We Comparing?

The dashboard compares the routes selected by the two approaches under the same simulated network conditions.

The comparison includes:

* Selected route
* Total number of hops
* Individual link costs
* Total weighted path cost
* Weighted-cost reduction
* Route changes following network-condition updates

To calculate weighted-cost reduction fairly, the dashboard evaluates the route selected by the shortest-hop baseline using the same RIPGuard cost formula used to evaluate the RIPGuard route.

This means the percentage represents a reduction in the **simulated weighted-cost metric**. It does not automatically represent the same percentage improvement in actual throughput, latency, or packet delivery.

## Network Topology

The dashboard models six routers representing the following locations:

| Router | Location    |
| ------ | ----------- |
| R1     | Head Office |
| R2     | Chennai     |
| R3     | Bangalore   |
| R4     | Hyderabad   |
| R5     | Mumbai      |
| R6     | Delhi       |

The network contains ten inter-router links. A route may use a direct connection or travel through multiple routers to reach its destination.

When a link fails, it is excluded from route calculation. The dashboard then recalculates the available route.

## Getting Started

You can run RIPGuard locally on your computer.

### Requirements

* Python 3.10 or later is recommended.
* No third-party Python packages are required.
* A modern web browser.

### Installation and Setup

**Step 1: Clone the repository**

```bash
git clone https://github.com/ashutoshsakolkar/RIPGuard.git
```

**Step 2: Open the project folder**

```bash
cd RIPGuard
```

**Step 3: Start the dashboard**

```bash
python dashboard.py
```

**Step 4: Open the dashboard**

Visit the following address in your browser:

```text
http://127.0.0.1:8770/
```

The dashboard should load locally.

To stop the server, return to the terminal and press `Ctrl+C`.

## Deploying the Dashboard

Uploading the source code to GitHub makes the project available for others to inspect and download. However, GitHub does not automatically run this Python application as a live website.

To provide a public dashboard link, the application must be deployed to a hosting service.

For a Render web service, use these settings:

| Setting       | Value                             |
| ------------- | --------------------------------- |
| Repository    | `ashutoshsakolkar/RIPGuard`       |
| Branch        | `main`                            |
| Runtime       | Python                            |
| Build command | `pip install -r requirements.txt` |
| Start command | `python dashboard.py`             |

After deployment, test the URL provided by the hosting service. Once the dashboard loads successfully, replace the live-demo notice at the top of this README with the verified public URL.

## Project Structure

```text
RIPGuard/
├── dashboard.py
├── README.md
├── requirements.txt
└── .gitignore
```

* `dashboard.py` contains the Python web server, dashboard interface, routing calculations, and interactive controls.
* `README.md` explains the project and how to run it.
* `requirements.txt` documents the dependency setup.
* `.gitignore` lists files that should not be committed to GitHub.

## Scope and Limitations

RIPGuard is currently a routing simulation rather than a live implementation of the RIP protocol.

The baseline models shortest-hop route selection. It does not exchange actual RIP routing updates between physical or emulated routers.

The latency, packet-loss, and utilization values are simulated. Therefore, dashboard results demonstrate the behaviour of the routing model under the selected conditions; they are not measurements from a production network.

A more complete evaluation could use a network emulator or real routing implementation to measure convergence time, packet delivery, end-to-end delay, and behaviour during link failures.

These additional tests would help establish how the approach performs beyond the current simulation.

## Why This Project?

I wanted to make routing decisions easier to understand and demonstrate visually.

Instead of simply displaying a routing table, RIPGuard allows users to change network conditions, observe the effect on link costs, and understand why an alternative route might become preferable.

The central idea behind the project is straightforward:

**The route with the fewest hops is not necessarily the route with the lowest weighted cost. By considering link conditions, a routing strategy can make different decisions when reliability and congestion matter.**
