RIPGuard — Reliability-Aware Routing Dashboard

RIPGuard is an interactive Python web dashboard that demonstrates and compares shortest-hop routing with a custom reliability-aware weighted-routing strategy in a six-router network.

🔗 Live Dashboard


https://YOUR-RIPGUARD-SERVICE.onrender.com

The GitHub repository contains the source code. The dashboard itself becomes publicly accessible only after the Python web app is deployed to a hosting service.

Repository

GitHub: https://github.com/ashutoshsakolkar/RIPGuard

Main application: dashboard.py

Features

Interactive six-router topology with ten links.

Dynamic per-link latency, packet-loss, and utilization metrics.

Calculated weighted link costs, shown in the topology and link table.

Side-by-side comparison of a shortest-hop RIP-style baseline and RIPGuard's weighted route selection.

Link failure and restoration controls with automatic route recalculation.

Controlled demonstration of high packet loss and threshold-based cost penalties.

Expandable link-cost calculations, event log, and route summary.

RIPGuard cost model

The project uses the following custom weighted cost:

C = 1 + 0.4L + 5P + 0.05U + S(P) + G(U)

S(P) = 0                         when P <= 10
       60 + 6(P - 10)            when P > 10

G(U) = 0                         when U <= 80
       0.15(U - 80)^2            when U > 80

Where:

L = latency in milliseconds.

P = packet loss in percentage points; for example, 12 means 12%.

U = link utilization in percentage points.

S(P) = additional packet-loss penalty.

G(U) = additional congestion penalty.

The 10% packet-loss threshold, 80% utilization threshold, and penalty coefficients are project-specific simulation choices, not universal networking standards.

Run locally

Requirements: Python 3.10 or later recommended. The application uses Python's standard library and does not require third-party packages.

Clone the repository:

git clone https://github.com/ashutoshsakolkar/RIPGuard.git
cd RIPGuard

Run the dashboard:

python dashboard.py

Open http://127.0.0.1:8770/ in a browser.

Press Ctrl+C in the terminal to stop the server.

Deploy publicly on Render

Push dashboard.py, README.md, requirements.txt, and .gitignore to the main branch of this GitHub repository.

Sign in to Render and choose New → Web Service.

Connect the GitHub repository ashutoshsakolkar/RIPGuard.

Use these settings:

Runtime: Python 3

Build command: pip install -r requirements.txt

Start command: python dashboard.py

Branch: main

Create the service and wait for the deployment to complete.

Open the Render-generated https://...onrender.com URL and confirm the dashboard loads.

Replace the pending URL near the top of this README with that real public URL, then commit and push the README update.

The application reads the PORT environment variable and binds to 0.0.0.0, as expected by Render web services.

Important scope note

RIPGuard is a routing simulation. The baseline models shortest-hop route selection; it does not run the actual RIP protocol between physical or emulated routers or exchange RIP routing updates. RIPGuard's weighted score is a custom metric, whereas standard RIP's native routing metric is hop count. Dashboard and benchmark figures are simulation outputs, not measurements from a production network.
