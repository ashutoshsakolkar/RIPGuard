# RIPGuard: Six-Router Network Topology

ROUTERS = ["R1", "R2", "R3", "R4", "R5", "R6"]

# Each link contains:
# latency_ms, packet_loss_pct, utilization_pct

LINKS = [
    {
        "source": "R1",
        "target": "R2",
        "latency_ms": 20,
        "packet_loss_pct": 1,
        "utilization_pct": 35,
    },
    {
        "source": "R2",
        "target": "R3",
        "latency_ms": 25,
        "packet_loss_pct": 1,
        "utilization_pct": 45,
    },
    {
        "source": "R3",
        "target": "R6",
        "latency_ms": 30,
        "packet_loss_pct": 2,
        "utilization_pct": 55,
    },
    {
        "source": "R1",
        "target": "R4",
        "latency_ms": 15,
        "packet_loss_pct": 1,
        "utilization_pct": 30,
    },
    {
        "source": "R4",
        "target": "R5",
        "latency_ms": 20,
        "packet_loss_pct": 1,
        "utilization_pct": 40,
    },
    {
        "source": "R5",
        "target": "R6",
        "latency_ms": 20,
        "packet_loss_pct": 1,
        "utilization_pct": 30,
    },
    {
        "source": "R2",
        "target": "R5",
        "latency_ms": 35,
        "packet_loss_pct": 3,
        "utilization_pct": 70,
    },
    {
        "source": "R3",
        "target": "R4",
        "latency_ms": 40,
        "packet_loss_pct": 2,
        "utilization_pct": 60,
    },
]