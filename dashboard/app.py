import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Render provides PORT as an environment variable.
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8770"))

PAGE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>RIPGuard | Six-Router Network</title>

<style>
:root {
    --bg: #f3f2e9;
    --card: #fffef9;
    --topo: #e5eadf;
    --ink: #29332b;
    --muted: #687568;
    --line: #cdd6c8;
    --green: #398052;
    --red: #b83c43;
    --olive: #65784f;
    --blue: #476c8e;
}

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font: 14px "Segoe UI", Arial, sans-serif;
}

header {
    padding: 20px 26px;
    background: #e8e9dd;
    border-bottom: 1px solid var(--line);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
}

h1 {
    font-size: 23px;
    margin: 0;
}

h2 {
    font-size: 16px;
    margin: 0 0 13px;
}

.muted, small {
    color: var(--muted);
}

main {
    max-width: 1450px;
    margin: auto;
    padding: 20px;
}

.metrics {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
}

.metric, .card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 11px;
    padding: 15px;
    margin-bottom: 14px;
}

.label {
    font-size: 10px;
    letter-spacing: .8px;
    color: var(--muted);
    font-weight: 700;
}

.value {
    font-size: 25px;
    font-weight: 750;
    margin: 7px 0;
}

.up {
    color: var(--green);
}

.down {
    color: var(--red);
}

.layout {
    display: grid;
    grid-template-columns: 1.45fr 1fr;
    gap: 14px;
}

.topo {
    width: 100%;
    background: var(--topo);
    border: 1px solid var(--line);
    border-radius: 9px;
}

.link {
    stroke: var(--green);
    stroke-width: 5;
    stroke-linecap: round;
    cursor: pointer;
}

.link.down {
    stroke: var(--red);
    stroke-width: 7;
    stroke-dasharray: 9 7;
}

.link.selected {
    stroke: var(--blue);
    stroke-width: 7;
}

.node rect {
    fill: #fffef9;
    stroke: #81947b;
    stroke-width: 2;
}

.node text {
    fill: var(--ink);
    text-anchor: middle;
}

.node .sub {
    fill: var(--muted);
    font-size: 10px;
}

.node.down rect {
    stroke: var(--red);
}

.edge-label {
    font-size: 10px;
    fill: #29332b;
    font-weight: 700;
    text-anchor: middle;
    paint-order: stroke;
    stroke: var(--topo);
    stroke-width: 4px;
    stroke-linejoin: round;
}

button, select {
    font: inherit;
    border: 1px solid #bdcbb8;
    border-radius: 7px;
    background: #eef1e8;
    color: var(--ink);
    padding: 9px 10px;
    cursor: pointer;
}

button:hover {
    filter: brightness(.97);
}

button.primary {
    background: var(--olive);
    color: white;
    border-color: var(--olive);
}

button.red {
    background: #fae7e5;
    color: #922d32;
    border-color: #dfaaa7;
}

button.green {
    background: #e4f0e3;
    color: #28663b;
    border-color: #b7d3b6;
}

.controls {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}

.controls label {
    display: block;
    font-size: 11px;
    font-weight: 700;
    color: var(--muted);
    margin-bottom: 6px;
}

.controls select,
.controls button {
    width: 100%;
    margin-bottom: 8px;
}

.actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-top: 6px;
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
}

th, td {
    text-align: left;
    padding: 9px 6px;
    border-bottom: 1px solid #e1e5dc;
}

th {
    color: var(--muted);
}

.tablewrap {
    overflow: auto;
}

.events {
    max-height: 200px;
    overflow: auto;
}

.event {
    padding: 7px 0;
    border-bottom: 1px solid #e1e5dc;
    font-size: 12px;
}

.time {
    color: var(--muted);
    margin-right: 7px;
}

.summary {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
}

.summary-item {
    background: #f0f2e9;
    border: 1px solid var(--line);
    border-radius: 8px;
    padding: 11px;
}

.summary-item b {
    display: block;
    margin-top: 5px;
    font-size: 15px;
    overflow-wrap: anywhere;
}

.comparison-wrap { overflow-x: auto; margin-top: 14px; }
.comparison-table { min-width: 520px; }
.comparison-table th:nth-child(2) { color: #476c8e; }
.comparison-table th:nth-child(3) { color: #398052; }
.comparison-table td { vertical-align: top; overflow-wrap: anywhere; }
.comparison-table td:first-child { font-weight: 700; min-width: 105px; }
.comparison-note { font-size: 11px; margin-top: 8px; line-height: 1.5; }
.comparison-kpis { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; margin: 12px 0; }
.comparison-kpi { background: #f0f2e9; border: 1px solid var(--line); border-radius: 8px; padding: 10px; min-width: 0; }
.comparison-kpi small { display: block; line-height: 1.4; }
.comparison-kpi b { display: block; margin-top: 5px; font-size: 17px; overflow-wrap: anywhere; }
.improvement-banner { background: #e7f2e5; border: 1px solid #b8d4b6; border-left: 5px solid var(--green); border-radius: 9px; padding: 13px; margin: 12px 0; }
.improvement-banner .value { font-size: 28px; margin: 4px 0; }
.improvement-banner p { margin: 5px 0 0; line-height: 1.5; font-size: 12px; }
@media(max-width: 520px) { .comparison-kpis { grid-template-columns: 1fr; } }
.loss-alert {
    display: none;
    background: #fff0e9;
    border: 1px solid #dc9a7b;
    border-left: 5px solid #b83c43;
    border-radius: 8px;
    padding: 11px 12px;
    margin: 12px 0 0;
    line-height: 1.5;
    font-size: 12px;
}
.formula-intro { background: #f0f2e9; padding: 12px; border-radius: 8px; line-height: 1.6; }
.formula-list { margin-top: 12px; }
.formula-detail { border: 1px solid var(--line); border-radius: 8px; margin: 8px 0; overflow: hidden; background: #fffef9; }
.formula-detail summary { cursor: pointer; padding: 11px; font-weight: 700; background: #f0f2e9; }
.formula-body { padding: 11px; font-size: 12px; line-height: 1.7; overflow-wrap: anywhere; }
.formula-equation { font-family: Consolas, "Courier New", monospace; font-weight: 700; background: #f7f8f2; padding: 8px; border-radius: 6px; }
.threshold-pill { display: inline-block; padding: 2px 6px; border-radius: 5px; background: #fae7e5; color: #922d32; font-weight: 700; }

.foot {
    padding: 8px;
    text-align: center;
    color: var(--muted);
    font-size: 11px;
}

@media(max-width: 900px) {
    .layout {
        grid-template-columns: 1fr;
    }

    .metrics {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media(max-width: 520px) {
    .comparison-grid { grid-template-columns: 1fr; }
    main {
        padding: 11px;
    }

    .controls {
        grid-template-columns: 1fr;
    }

    .summary {
        grid-template-columns: repeat(2, 1fr);
    }

    header {
        padding: 16px;
    }
}
</style>
</head>

<body>

<header>
    <div>
        <h1>RIPGuard <span style="color:#65784f">/ Network Recovery</span></h1>
        <small>Six-router network · weighted route selection · link-failure recovery</small>
    </div>
    <div>
        <b id="headerStatus" class="up">● Network connected</b>
    </div>
</header>

<main>

<div class="metrics">

    <div class="metric">
        <div class="label">ROUTERS</div>
        <div class="value" id="routerCount">6</div>
        <small>Head Office and five branches</small>
    </div>

    <div class="metric">
        <div class="label">ACTIVE LINKS</div>
        <div class="value" id="linkCount">10 / 10</div>
        <small>Available connections</small>
    </div>

    <div class="metric">
        <div class="label">SELECTED ROUTE</div>
        <div class="value" id="topStatus">CONNECTED</div>
        <small id="topStatusNote">Source can reach destination</small>
    </div>

    <div class="metric">
        <div class="label">LAST ACTION</div>
        <div class="value" id="lastAction">Ready</div>
        <small>Most recent network change</small>
    </div>

</div>

<div class="layout">

<div>

<section class="card">

<h2>1. Network topology <span class="muted">— click a link to select it</span></h2>

<svg class="topo" viewBox="0 0 700 360" role="img"
     aria-label="Six router weighted network topology">

<!-- Ten connections -->

<line id="e12" class="link"
x1="175" y1="75" x2="300" y2="75"
onclick="selectLink('R1-R2')"/>

<line id="e23" class="link"
x1="400" y1="75" x2="525" y2="75"
onclick="selectLink('R2-R3')"/>

<line id="e34" class="link"
x1="585" y1="110" x2="585" y2="245"
onclick="selectLink('R3-R4')"/>

<line id="e45" class="link"
x1="525" y1="280" x2="400" y2="280"
onclick="selectLink('R4-R5')"/>

<line id="e56" class="link"
x1="300" y1="280" x2="175" y2="280"
onclick="selectLink('R5-R6')"/>

<line id="e61" class="link"
x1="115" y1="245" x2="115" y2="110"
onclick="selectLink('R6-R1')"/>

<line id="e14" class="link"
x1="155" y1="105" x2="545" y2="250"
onclick="selectLink('R1-R4')"/>

<line id="e25" class="link"
x1="350" y1="110" x2="350" y2="245"
onclick="selectLink('R2-R5')"/>

<line id="e36" class="link"
x1="545" y1="105" x2="155" y2="250"
onclick="selectLink('R3-R6')"/>

<line id="e26" class="link"
x1="315" y1="105" x2="150" y2="250"
onclick="selectLink('R2-R6')"/>

<!-- Link costs -->

<text id="label12" class="edge-label" x="238" y="59"></text>
<text id="label23" class="edge-label" x="462" y="59"></text>
<text id="label34" class="edge-label" x="612" y="174"></text>
<text id="label45" class="edge-label" x="462" y="300"></text>
<text id="label56" class="edge-label" x="238" y="300"></text>
<text id="label61" class="edge-label" x="87" y="179"></text>
<text id="label14" class="edge-label" x="245" y="125"></text>
<text id="label25" class="edge-label" x="378" y="137"></text>
<text id="label36" class="edge-label" x="475" y="129"></text>
<text id="label26" class="edge-label" x="236" y="171"></text>

<!-- Router 1 -->

<g class="node" id="n1" transform="translate(65 40)">
    <rect width="100" height="70" rx="10"/>
    <text x="50" y="25">R1 · HO</text>
    <text class="sub" x="50" y="43">Head Office</text>
    <text class="sub" x="50" y="57">192.168.1.0/24</text>
</g>

<!-- Router 2 -->

<g class="node" id="n2" transform="translate(300 40)">
    <rect width="100" height="70" rx="10"/>
    <text x="50" y="25">R2</text>
    <text class="sub" x="50" y="43">Chennai</text>
    <text class="sub" x="50" y="57">192.168.2.0/24</text>
</g>

<!-- Router 3 -->

<g class="node" id="n3" transform="translate(535 40)">
    <rect width="100" height="70" rx="10"/>
    <text x="50" y="25">R3</text>
    <text class="sub" x="50" y="43">Bangalore</text>
    <text class="sub" x="50" y="57">192.168.3.0/24</text>
</g>

<!-- Router 4 -->

<g class="node" id="n4" transform="translate(535 245)">
    <rect width="100" height="70" rx="10"/>
    <text x="50" y="25">R4</text>
    <text class="sub" x="50" y="43">Hyderabad</text>
    <text class="sub" x="50" y="57">192.168.4.0/24</text>
</g>

<!-- Router 5 -->

<g class="node" id="n5" transform="translate(300 245)">
    <rect width="100" height="70" rx="10"/>
    <text x="50" y="25">R5</text>
    <text class="sub" x="50" y="43">Mumbai</text>
    <text class="sub" x="50" y="57">192.168.5.0/24</text>
</g>

<!-- Router 6 -->

<g class="node" id="n6" transform="translate(65 245)">
    <rect width="100" height="70" rx="10"/>
    <text x="50" y="25">R6</text>
    <text class="sub" x="50" y="43">Delhi</text>
    <text class="sub" x="50" y="57">192.168.6.0/24</text>
</g>

</svg>

<p class="muted">
Green = active link · Red = failed link. Each connection shows its name and cost on separate lines. RIPGuard prefers the lowest total weighted cost.
</p>

</section>

<section class="card">

<h2>2. Link metrics and calculated costs</h2>

<div class="actions" style="margin-bottom:10px">
    <button class="primary" onclick="randomizeMetrics()">Generate random network conditions</button>
    <button class="red" onclick="simulateHighLoss()">Demo route change at &gt;10% packet loss</button>
    <button onclick="resetMetrics()">Reset metrics</button>
</div>
<small style="display:block;margin-bottom:10px">Cost = 1 + (0.4 × latency in ms) + (5 × packet loss %) + (0.05 × utilization %). Random packet loss ranges from 0% to 20%, so values above 10% can occur.</small>
<div id="packetLossAlert" class="loss-alert" role="status" aria-live="polite"></div>

<div class="tablewrap">
<table>
<thead>
<tr>
    <th>Connection</th>
    <th>Latency</th>
    <th>Packet loss</th>
    <th>Utilization</th>
    <th>Calculated cost</th>
    <th>Status</th>
    <th>Action</th>
</tr>
</thead>
<tbody id="linkRows"></tbody>
</table>
</div>

</section>

<section class="card">
<h2>3. Standard RIP vs RIPGuard — route performance</h2>
<p class="muted" style="margin-top:-4px;line-height:1.5">
Both methods use the same active network. Standard RIP selects the route with the fewest hops; RIPGuard selects the route with the lowest calculated weighted cost.
</p>

<div class="improvement-banner">
    <div class="label">RIPGUARD WEIGHTED-COST REDUCTION VS THE RIP-SELECTED PATH</div>
    <div class="value" id="improvementPercent">—</div>
    <p id="improvementExplanation">Choose a source and destination to compare both routes.</p>
</div>

<div class="comparison-kpis">
    <div class="comparison-kpi"><small>Standard RIP hop count</small><b id="ripHopsKpi">—</b></div>
    <div class="comparison-kpi"><small>RIP path cost on the same weighted scale</small><b id="ripWeightedCostKpi">—</b></div>
    <div class="comparison-kpi"><small>RIPGuard weighted path cost</small><b id="guardWeightedCostKpi">—</b></div>
</div>

<div class="comparison-wrap">
    <table class="comparison-table">
        <thead><tr><th>Metric</th><th>Standard RIP</th><th>RIPGuard</th></tr></thead>
        <tbody id="routingComparisonRows"></tbody>
    </table>
</div>

<p class="muted comparison-note">
Fair comparison note: standard RIP's native metric is hop count, not this weighted cost. To calculate the percentage shown above, the dashboard evaluates the path selected by RIP using RIPGuard's link-cost formula, then compares that value with RIPGuard's selected path cost. This is a simulated weighted-cost improvement, not a claim that standard RIP natively uses latency, packet loss, or utilization.
</p>
</section>

</div>

<div>

<section class="card">

<h2>4. Choose route</h2>

<div class="controls">

<div>
<label for="source">SOURCE ROUTER</label>
<select id="source">
    <option value="1">R1 — Head Office</option>
    <option value="2">R2 — Chennai</option>
    <option value="3">R3 — Bangalore</option>
    <option value="4" selected>R4 — Hyderabad</option>
    <option value="5">R5 — Mumbai</option>
    <option value="6">R6 — Delhi</option>
</select>
</div>

<div>
<label for="destination">DESTINATION ROUTER</label>
<select id="destination">
    <option value="3" selected>R3 — Bangalore</option>
    <option value="1">R1 — Head Office</option>
    <option value="2">R2 — Chennai</option>
    <option value="4">R4 — Hyderabad</option>
    <option value="5">R5 — Mumbai</option>
    <option value="6" selected>R6 — Delhi</option>
</select>
</div>

</div>

<button class="primary" style="width:100%"
onclick="calculateRoute()">
Calculate lowest-cost route
</button>

<hr style="border:0;border-top:1px solid #e1e5dc;margin:15px 0">

<div class="label">SELECTED ROUTE</div>

<div id="routeText"
style="font-size:19px;font-weight:750;margin:8px 0">
R1 → R2 → R5 → R4 → R3
</div>

<div id="routeExplanation" class="muted">
Calculating best available route…
</div>

<div class="actions">
    <button class="green" onclick="restoreAll()">Restore all links</button>
    <button onclick="testConnection()">Test connectivity</button>
    <button onclick="resetNetwork()">Reset network</button>
</div>

</section>

<section class="card">

<h2>5. Link failure controls</h2>

<label class="muted" for="linkChoice">
Select a connection to fail or restore
</label>

<select id="linkChoice" style="width:100%;margin:8px 0 10px"></select>

<div class="actions">
    <button class="red" onclick="toggleSelectedLink()">
        Fail / restore selected link
    </button>
</div>

<p class="muted">
You can also click any connection in the topology or table.
</p>

</section>

<section class="card">

<h2>
6. Event log
<button style="float:right" onclick="clearLog()">Clear log</button>
</h2>

<div class="events" id="events"></div>

</section>

<section class="card">

<h2>7. Route summary</h2>

<div class="summary">

<div class="summary-item">
    <small>Source → Destination</small>
    <b id="sumPair">R4 → R6</b>
</div>

<div class="summary-item">
    <small>Hops</small>
    <b id="sumHops">—</b>
</div>

<div class="summary-item">
    <small>Total link cost</small>
    <b id="sumCost">—</b>
</div>

<div class="summary-item">
    <small>Connection</small>
    <b id="sumStatus">Connected</b>
</div>

<div class="summary-item">
    <small>Route selected</small>
    <b id="sumRoute">R4 → R5 → R6</b>
</div>

<div class="summary-item">
    <small>Last test</small>
    <b id="sumTest">Not tested</b>
</div>

</div>
</section>

<section class="card">

<h2>8. Cost formula and per-link calculation</h2>

<div class="formula-intro">
    <b>RIPGuard link-cost formula</b><br>
    <span class="formula-equation">C = 1 + (0.4 × L) + (5 × P) + (0.05 × U)</span><br>
    <small>L = latency in milliseconds; P = packet loss percentage (for example, 15 means 15%); U = link utilization percentage.</small><br>
    <small>Each connection below can be expanded or minimized. Clicking a link in the topology or link table selects and opens its calculation.</small>
</div>

<div id="linkCalculations" class="formula-list"></div>

</section>

</div>
</div>

<div class="foot">
RIPGuard · Weighted path demonstration with six routers
</div>

</main>

<script>
const N = {
    1: 'R1 — Head Office',
    2: 'R2 — Chennai',
    3: 'R3 — Bangalore',
    4: 'R4 — Hyderabad',
    5: 'R5 — Mumbai',
    6: 'R6 — Delhi'
};

const L = {
    'R1-R2': {a:1, b:2, cost:0, latency:35, loss:1.0, util:35, up:true, svg:'e12', label:'label12'},
    'R2-R3': {a:2, b:3, cost:0, latency:42, loss:0.5, util:48, up:true, svg:'e23', label:'label23'},
    'R3-R4': {a:3, b:4, cost:0, latency:28, loss:1.2, util:30, up:true, svg:'e34', label:'label34'},
    'R4-R5': {a:4, b:5, cost:0, latency:50, loss:2.0, util:62, up:true, svg:'e45', label:'label45'},
    'R5-R6': {a:5, b:6, cost:0, latency:22, loss:0.2, util:25, up:true, svg:'e56', label:'label56'},
    'R6-R1': {a:6, b:1, cost:0, latency:60, loss:3.0, util:70, up:true, svg:'e61', label:'label61'},
    'R1-R4': {a:1, b:4, cost:0, latency:75, loss:2.5, util:80, up:true, svg:'e14', label:'label14'},
    'R2-R5': {a:2, b:5, cost:0, latency:30, loss:0.8, util:40, up:true, svg:'e25', label:'label25'},
    'R3-R6': {a:3, b:6, cost:0, latency:55, loss:1.5, util:58, up:true, svg:'e36', label:'label36'},
    'R2-R6': {a:2, b:6, cost:0, latency:45, loss:1.0, util:50, up:true, svg:'e26', label:'label26'}
};

let events = [];
let faults = 0;
let restores = 0;
let tests = 0;
let successes = 0;
let lastTest = 'Not tested';
let lastRoute = null;
let selectedLink = 'R1-R2';

// RIPGuard uses a custom weighted metric; standard RIP uses hop count.
function calculateLinkCost(link) {
    return Math.round((1 + 0.4 * link.latency + 5 * link.loss + 0.05 * link.util) * 100) / 100;
}

const BASELINE_METRICS = {
    'R1-R2': {latency:35, loss:1.0, util:35},
    'R2-R3': {latency:42, loss:0.5, util:48},
    'R3-R4': {latency:28, loss:1.2, util:30},
    'R4-R5': {latency:50, loss:2.0, util:62},
    'R5-R6': {latency:22, loss:0.2, util:25},
    'R6-R1': {latency:60, loss:3.0, util:70},
    'R1-R4': {latency:75, loss:2.5, util:80},
    'R2-R5': {latency:30, loss:0.8, util:40},
    'R3-R6': {latency:55, loss:1.5, util:58},
    'R2-R6': {latency:45, loss:1.0, util:50}
};

function restoreBaselineMetrics() {
    for (const [key, values] of Object.entries(BASELINE_METRICS)) {
        Object.assign(L[key], values);
    }
    updateAllLinkCosts();
}

function updateAllLinkCosts() {
    for (const link of Object.values(L)) {
        link.cost = calculateLinkCost(link);
    }
}

function updateMetricLabels() {
    for (const link of Object.values(L)) {
        const label = document.getElementById(link.label);
        if (!label) continue;
        const x = label.getAttribute('x');
        label.innerHTML = `<tspan x="${x}" dy="0">R${link.a}–R${link.b}</tspan><tspan x="${x}" dy="12">Cost: ${link.cost.toFixed(2)}</tspan>`;
    }
}

function pathText(route) {
    return route ? route.nodes.map(n => 'R' + n).join(' → ') : 'No route available';
}

function routeSignature(route) {
    return route ? route.nodes.join('-') : 'NO-ROUTE';
}

// Generate random values in a deliberately broad range so the >10% loss threshold
// can be demonstrated without repeatedly clicking and hoping for a rare value.
function randomizeMetrics() {
    const start = Number(source.value);
    const end = Number(destination.value);
    const oldRoute = getRoute(start, end);

    for (const link of Object.values(L)) {
        link.latency = Math.floor(Math.random() * 81) + 20; // 20–100 ms
        link.loss = Number((Math.random() * 20).toFixed(2)); // 0–20%; often crosses 10%
        link.util = Math.floor(Math.random() * 76) + 15; // 15–90%
    }

    updateAllLinkCosts();
    renderRoute();
    const newRoute = getRoute(start, end);
    showPacketLossAlert(oldRoute, newRoute, 'random');
    document.getElementById('lastAction').textContent = 'Metrics updated';

    const highLinks = Object.entries(L).filter(([, link]) => link.loss > 10);
    if (highLinks.length) {
        log(`Packet-loss threshold alert: ${highLinks.map(([key, link]) => `${key} ${link.loss.toFixed(2)}%`).join(', ')}. RIPGuard recalculated the route using the new weighted costs.`, 'warn');
    } else {
        log('Random latency, packet-loss and utilization values generated. Costs and routes recalculated.', 'good');
    }
}

function resetMetrics() {
    restoreBaselineMetrics();
    renderRoute();
    const alert = document.getElementById('packetLossAlert');
    alert.style.display = 'none';
    alert.textContent = '';
    document.getElementById('lastAction').textContent = 'Metrics reset';
    log('Baseline metrics restored for all ten links.', 'good');
}

// Deterministic teacher-demo: under baseline conditions R1→R3 uses R1-R2-R3.
// Raising only R1-R2 loss to 15% makes the R1-R4-R3 alternative cheaper.
function simulateHighLoss() {
    for (const link of Object.values(L)) link.up = true;
    restoreBaselineMetrics();
    source.value = '1';
    destination.value = '3';

    const oldRoute = getRoute(1, 3);
    const affected = L['R1-R2'];
    affected.loss = 15.00;
    selectedLink = 'R1-R2';
    linkChoice.value = selectedLink;
    updateAllLinkCosts();
    renderRoute();
    const newRoute = getRoute(1, 3);

    const alert = document.getElementById('packetLossAlert');
    alert.style.display = 'block';
    alert.innerHTML = `<b>PACKET-LOSS THRESHOLD EXCEEDED</b><br>R1–R2 packet loss is ${affected.loss.toFixed(2)}%, above the 10% threshold. Its calculated cost is now ${affected.cost.toFixed(2)}. RIPGuard changed the route from <b>${pathText(oldRoute)}</b> to <b>${pathText(newRoute)}</b> after recalculation. Other baseline link metrics were held constant for this demonstration.`;

    document.getElementById('lastAction').textContent = 'High-loss route change';
    log(`Controlled demo: R1-R2 packet loss raised to 15.00% (>10% threshold). RIPGuard route changed from ${pathText(oldRoute)} to ${pathText(newRoute)}; R1-R2 cost is ${affected.cost.toFixed(2)}.`, 'warn');
}

function showPacketLossAlert(oldRoute, newRoute, mode) {
    const alert = document.getElementById('packetLossAlert');
    const highLinks = Object.entries(L).filter(([, link]) => link.loss > 10);
    if (!highLinks.length) {
        alert.style.display = 'none';
        alert.textContent = '';
        return;
    }

    const highText = highLinks.map(([key, link]) => `${key} (${link.loss.toFixed(2)}%)`).join(', ');
    const changed = routeSignature(oldRoute) !== routeSignature(newRoute);
    alert.style.display = 'block';
    if (changed) {
        alert.innerHTML = `<b>PACKET-LOSS WARNING — ROUTE RECALCULATED</b><br>Loss above 10% detected on ${highText}. The selected path changed from <b>${pathText(oldRoute)}</b> to <b>${pathText(newRoute)}</b> after the latest network metrics were applied.`;
    } else {
        alert.innerHTML = `<b>PACKET-LOSS WARNING</b><br>Loss above 10% detected on ${highText}. RIPGuard recalculated the path; it remains <b>${pathText(newRoute)}</b> because it still has the lowest available weighted cost.`;
    }
}

function getRipRoute(start, end) {
    start = Number(start);
    end = Number(end);
    if (start === end) return {nodes:[start], links:[], hops:0};

    const queue = [start];
    const visited = new Set([start]);
    const previous = {};
    const previousLink = {};

    while (queue.length) {
        const u = queue.shift();
        for (const [key, link] of Object.entries(L)) {
            if (!link.up) continue;
            const v = link.a === u ? link.b : (link.b === u ? link.a : null);
            if (v === null || visited.has(v)) continue;
            visited.add(v);
            previous[v] = u;
            previousLink[v] = key;
            queue.push(v);
            if (v === end) {
                queue.length = 0;
                break;
            }
        }
    }

    if (!visited.has(end)) return null;
    const nodes = [end];
    const links = [];
    let current = end;
    while (current !== start) {
        links.unshift(previousLink[current]);
        current = previous[current];
        nodes.unshift(current);
    }
    return {nodes, links, hops: links.length};
}

function updateRoutingComparison() {
    const start = Number(source.value);
    const end = Number(destination.value);
    const rip = getRipRoute(start, end);       // Breadth-first search: minimum hop count
    const guard = getRoute(start, end);        // Dijkstra: minimum RIPGuard weighted cost

    // Re-evaluate the path chosen by standard RIP with RIPGuard's weights so both
    // paths can be compared on the same scale. This is not standard RIP's own metric.
    const ripWeightedCost = rip
        ? rip.links.reduce((sum, key) => sum + L[key].cost, 0)
        : null;
    const guardWeightedCost = guard ? guard.cost : null;

    let improvement = null;
    if (rip && guard && ripWeightedCost > 0) {
        improvement = ((ripWeightedCost - guardWeightedCost) / ripWeightedCost) * 100;
        // Both paths use the same active graph and weights, so Dijkstra should not
        // have a greater weighted cost than the RIP-selected path.
        if (improvement < 0 && improvement > -0.0001) improvement = 0;
    }

    const ripPathCostText = rip
        ? `${ripWeightedCost.toFixed(2)} weighted units`
        : 'Unavailable';
    const guardPathCostText = guard
        ? `${guardWeightedCost.toFixed(2)} weighted units`
        : 'Unavailable';

    document.getElementById('ripHopsKpi').textContent = rip ? rip.hops : 'No route';
    document.getElementById('ripWeightedCostKpi').textContent = rip ? ripWeightedCost.toFixed(2) : '—';
    document.getElementById('guardWeightedCostKpi').textContent = guard ? guardWeightedCost.toFixed(2) : '—';

    const percentElement = document.getElementById('improvementPercent');
    const explanationElement = document.getElementById('improvementExplanation');
    if (!rip || !guard) {
        percentElement.textContent = 'N/A';
        explanationElement.textContent = 'At least one method cannot reach the selected destination with the current active links.';
    } else if (start === end || ripWeightedCost === 0) {
        percentElement.textContent = 'N/A';
        explanationElement.textContent = 'Source and destination are the same router, so there is no path cost to compare.';
    } else {
        const safeImprovement = Math.max(0, improvement);
        percentElement.textContent = `${safeImprovement.toFixed(1)}%`;
        if (safeImprovement > 0.05) {
            explanationElement.textContent = `RIPGuard's selected route has ${safeImprovement.toFixed(1)}% lower weighted cost than the route standard RIP selected, when both paths are evaluated using the same RIPGuard formula.`;
        } else {
            explanationElement.textContent = 'Both selected paths have effectively the same weighted cost for this source and destination.';
        }
    }

    const ripBreakdown = rip && rip.links.length
        ? rip.links.map((key, i) => `R${rip.nodes[i]}–R${rip.nodes[i + 1]}: 1 hop · weighted cost ${L[key].cost.toFixed(2)}`).join('<br>')
        : (rip ? 'No links needed' : 'Unavailable');
    const guardBreakdown = guard && guard.links.length
        ? guard.links.map(key => `R${L[key].a}–R${L[key].b}: weighted cost ${L[key].cost.toFixed(2)}`).join('<br>')
        : (guard ? 'No links needed' : 'Unavailable');

    const hopDifference = (rip && guard)
        ? guard.links.length - rip.hops
        : null;
    let hopDifferenceText = 'Unavailable';
    if (hopDifference !== null) {
        if (hopDifference === 0) hopDifferenceText = 'Same number of hops';
        else if (hopDifference > 0) hopDifferenceText = `${hopDifference} more hop(s) than RIP`;
        else hopDifferenceText = `${Math.abs(hopDifference)} fewer hop(s) than RIP`;
    }

    const rows = [
        ['Selected route', pathText(rip), pathText(guard)],
        ['Total hops', rip ? rip.hops : 'No route', guard ? guard.links.length : 'No route'],
        ['Route-selection metric', rip ? `${rip.hops} hops (native RIP metric)` : 'Unavailable', guard ? `${guardWeightedCost.toFixed(2)} total weighted cost` : 'Unavailable'],
        ['Selected path cost on the same weighted scale', ripPathCostText, guardPathCostText],
        ['Per-link values on selected path', ripBreakdown, guardBreakdown],
        ['Hop-count difference', 'Baseline', hopDifferenceText],
        ['Weighted-cost reduction vs RIP-selected path', 'Baseline', improvement === null ? 'N/A' : `${Math.max(0, improvement).toFixed(1)}% lower weighted cost`]
    ];

    document.getElementById('routingComparisonRows').innerHTML = rows.map(([label, ripValue, guardValue]) =>
        `<tr><td>${label}</td><td>${ripValue}</td><td>${guardValue}</td></tr>`
    ).join('');
}

function renderFormulaDetails() {
    const container = document.getElementById('linkCalculations');
    if (!container) return;
    const previouslyOpen = new Set(
        [...container.querySelectorAll('details[open]')].map(item => item.dataset.key)
    );
    if (!previouslyOpen.size) previouslyOpen.add(selectedLink);

    container.innerHTML = Object.entries(L).map(([key, link]) => {
        const equation = `1 + (0.4 × ${link.latency}) + (5 × ${link.loss.toFixed(2)}) + (0.05 × ${link.util}) = ${link.cost.toFixed(2)}`;
        const threshold = link.loss > 10
            ? '<p class="down"><b>Warning:</b> packet loss exceeds the 10% threshold.</p>'
            : '<p class="muted">Packet loss is at or below the 10% threshold.</p>';
        return `<details class="formula-detail" data-key="${key}" id="calc-${key}" ${previouslyOpen.has(key) || key === selectedLink ? 'open' : ''}>
            <summary>R${link.a} ↔ R${link.b} · Cost ${link.cost.toFixed(2)}${link.loss > 10 ? ' · LOSS &gt;10%' : ''}</summary>
            <div class="formula-body">
                <div><b>Latency:</b> ${link.latency} ms &nbsp; <b>Packet loss:</b> ${link.loss.toFixed(2)}% &nbsp; <b>Utilization:</b> ${link.util}%</div>
                <div class="formula-equation">C = ${equation}</div>
                <div><b>Calculated link cost:</b> ${link.cost.toFixed(2)}</div>
                ${threshold}
            </div>
        </details>`;
    }).join('');
}

function log(msg, type = 'info') {
    events.unshift({
        time: new Date().toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: false
        }),
        msg,
        type
    });

    events = events.slice(0, 40);
    renderLog();
}

function getRoute(start, end) {
    start = Number(start);
    end = Number(end);

    if (start === end) {
        return {nodes:[start], cost:0, links:[]};
    }

    let dist = {};
    let prev = {};
    let prevLink = {};
    let visited = new Set();

    for (let i = 1; i <= 6; i++) {
        dist[i] = Infinity;
    }

    dist[start] = 0;

    // Dijkstra's algorithm calculates the lowest-cost route.
    while (true) {
        let u = null;

        for (let i = 1; i <= 6; i++) {
            if (
                !visited.has(i) &&
                (u === null || dist[i] < dist[u])
            ) {
                u = i;
            }
        }

        if (u === null || dist[u] === Infinity) {
            break;
        }

        if (u === end) {
            break;
        }

        visited.add(u);

        for (const [key, link] of Object.entries(L)) {
            if (!link.up) {
                continue;
            }

            let v = link.a === u
                ? link.b
                : link.b === u
                    ? link.a
                    : null;

            if (v === null || visited.has(v)) {
                continue;
            }

            let alt = dist[u] + link.cost;

            if (alt < dist[v]) {
                dist[v] = alt;
                prev[v] = u;
                prevLink[v] = key;
            }
        }
    }

    if (dist[end] === Infinity) {
        return null;
    }

    let nodes = [end];
    let links = [];
    let cur = end;

    while (cur !== start) {
        links.unshift(prevLink[cur]);
        cur = prev[cur];
        nodes.unshift(cur);
    }

    return {
        nodes,
        cost: dist[end],
        links
    };
}

function selected() {
    return getRoute(
        document.getElementById('source').value,
        document.getElementById('destination').value
    );
}

function calculateRoute() {
    const a = Number(document.getElementById('source').value);
    const b = Number(document.getElementById('destination').value);

    lastRoute = getRoute(a, b);

    renderRoute();

    log(
        lastRoute
            ? `Calculated lowest-cost route from R${a} to R${b}.`
            : `No route available from R${a} to R${b}.`,
        lastRoute ? 'good' : 'bad'
    );
}

function renderRoute() {
    const a = Number(document.getElementById('source').value);
    const b = Number(document.getElementById('destination').value);
    const r = getRoute(a, b);

    lastRoute = r;

    document.getElementById('topStatus').textContent =
        r ? 'CONNECTED' : 'NO ROUTE';

    document.getElementById('topStatus').className =
        'value ' + (r ? 'up' : 'down');

    document.getElementById('topStatusNote').textContent =
        r
            ? 'Source can reach destination'
            : 'No available path between selected routers';

    document.getElementById('headerStatus').textContent =
        r ? '● Network connected' : '● No route';

    document.getElementById('headerStatus').className =
        r ? 'up' : 'down';

    document.getElementById('routeText').textContent =
        r
            ? r.nodes.map(n => 'R' + n).join(' → ')
            : 'No route available';

    document.getElementById('routeExplanation').textContent =
        r
            ? `${r.nodes.length - 1} hop(s) · total cost ${r.cost.toFixed(2)} · ${r.links.length} active link(s) used.`
            : 'Restore a link or choose another destination.';

    document.getElementById('sumPair').textContent =
        'R' + a + ' → R' + b;

    document.getElementById('sumHops').textContent =
        r ? r.nodes.length - 1 : '—';

    document.getElementById('sumCost').textContent =
        r ? r.cost.toFixed(2) : '—';

    document.getElementById('sumStatus').textContent =
        r ? 'Connected' : 'No route';

    document.getElementById('sumStatus').className =
        r ? 'up' : 'down';

    document.getElementById('sumRoute').textContent =
        r
            ? r.nodes.map(n => 'R' + n).join(' → ')
            : 'Unavailable';

    document.getElementById('sumTest').textContent = lastTest;

    document.getElementById('linkCount').textContent =
        Object.values(L).filter(link => link.up).length +
        ' / ' + Object.keys(L).length;

    // Update link and router states in the topology.
    for (const [key, link] of Object.entries(L)) {
        const el = document.getElementById(link.svg);

        el.classList.toggle('down', !link.up);
        el.classList.toggle('selected', key === selectedLink);

        for (const router of [link.a, link.b]) {
            const hasActiveLink = Object.values(L).some(
                item =>
                    item.up &&
                    (item.a === router || item.b === router)
            );

            document.getElementById('n' + router)
                .classList.toggle('down', !hasActiveLink);
        }
    }

    updateMetricLabels();
    updateRoutingComparison();
    renderFormulaDetails();
    renderLinks();
}

function renderLinks() {
    document.getElementById('linkRows').innerHTML =
        Object.entries(L).map(([key, link]) => `
            <tr>
                <td>
                    <button onclick="selectLink('${key}')" style="padding:4px 7px">
                        R${link.a} ↔ R${link.b}
                    </button>
                </td>
                <td>${link.latency} ms</td>
                <td class="${link.loss > 10 ? 'down' : ''}">${link.loss.toFixed(2)}%${link.loss > 10 ? ' ⚠' : ''}</td>
                <td>${link.util}%</td>
                <td><b>${link.cost.toFixed(2)}</b></td>
                <td class="${link.up ? 'up' : 'down'}">● ${link.up ? 'UP' : 'DOWN'}</td>
                <td>
                    <button class="${link.up ? 'red' : 'green'}" onclick="toggleLink('${key}')">
                        ${link.up ? 'Fail' : 'Restore'}
                    </button>
                </td>
            </tr>
        `).join('');

    // Keep the link selector's displayed costs synchronized with the table.
    for (const option of document.getElementById('linkChoice').options) {
        const link = L[option.value];
        if (link) option.textContent = `R${link.a} ↔ R${link.b} (cost ${link.cost.toFixed(2)})`;
    }
}

function renderLog() {
    document.getElementById('events').innerHTML =
        events.map(event => `
            <div class="event">
                <span class="time">${event.time}</span>
                <b class="${
                    (event.type === 'bad' || event.type === 'warn')
                        ? 'down'
                        : event.type === 'good'
                            ? 'up'
                            : ''
                }">
                    ${
                        event.type === 'bad'
                            ? 'FAILURE'
                            : event.type === 'warn'
                                ? 'WARNING'
                                : event.type === 'good'
                                    ? 'RECOVERY'
                                    : 'EVENT'
                    }
                </b>
                · ${event.msg}
            </div>
        `).join('') || '<p class="muted">No events yet.</p>';
}

function selectLink(key) {
    selectedLink = key;
    document.getElementById('linkChoice').value = key;
    renderRoute();
    const detail = document.getElementById('calc-' + key);
    if (detail) detail.open = true;
}

function toggleSelectedLink() {
    toggleLink(document.getElementById('linkChoice').value);
}

function toggleLink(key) {
    selectedLink = key;

    document.getElementById('linkChoice').value = key;

    const link = L[key];

    if (link.up) {
        link.up = false;
        faults++;

        document.getElementById('lastAction').textContent =
            'Link failed';

        log(
            `R${link.a}–R${link.b} failed (cost ${link.cost}). Recalculating route.`,
            'bad'
        );
    } else {
        link.up = true;
        restores++;

        document.getElementById('lastAction').textContent =
            'Link restored';

        log(
            `R${link.a}–R${link.b} restored.`,
            'good'
        );
    }

    renderRoute();
}

function restoreAll() {
    let count = 0;

    for (const link of Object.values(L)) {
        if (!link.up) {
            link.up = true;
            restores++;
            count++;
        }
    }

    document.getElementById('lastAction').textContent =
        'Links restored';

    log(
        count
            ? count + ' failed link(s) restored.'
            : 'All links are already active.',
        count ? 'good' : 'info'
    );

    renderRoute();
}

function testConnection() {
    tests++;

    const route = selected();

    if (route) {
        successes++;
    }

    lastTest = route ? 'PASS' : 'FAIL';

    document.getElementById('sumTest').textContent = lastTest;

    log(
        `Connectivity test R${source.value} → R${destination.value}: ${lastTest}.`,
        route ? 'good' : 'bad'
    );

    renderRoute();
}

function resetNetwork() {
    for (const link of Object.values(L)) {
        link.up = true;
    }
    restoreBaselineMetrics();
    const lossAlert = document.getElementById('packetLossAlert');
    lossAlert.style.display = 'none';
    lossAlert.textContent = '';

    faults = 0;
    restores = 0;
    tests = 0;
    successes = 0;
    lastTest = 'Not tested';

    document.getElementById('lastAction').textContent = 'Reset';

    log(
        'Network reset. All ten links are active.',
        'good'
    );

    renderRoute();
}

function clearLog() {
    events = [];
    renderLog();
}

// Calculate initial costs, then populate the link selection dropdown.
updateAllLinkCosts();
for (const [key, link] of Object.entries(L)) {
    const option = document.createElement('option');

    option.value = key;
    option.textContent =
        `R${link.a} ↔ R${link.b} (cost ${link.cost})`;

    document.getElementById('linkChoice').appendChild(option);
}

// Connect dropdown changes to route calculation.
const source = document.getElementById('source');
const destination = document.getElementById('destination');
const linkChoice = document.getElementById('linkChoice');

source.onchange = calculateRoute;
destination.onchange = calculateRoute;
linkChoice.onchange = () => selectLink(linkChoice.value);

// Initialize the dashboard.
renderRoute();

log(
    'Network ready. Ten links are active across six routers.',
    'good'
);
</script>

</body>
</html>"""


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(f"Request received: {self.path}")

        if self.path.split("?")[0] in ("/", "/index.html"):
            data = PAGE.encode("utf-8")

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )
            self.send_header(
                "Content-Length",
                str(len(data))
            )
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        else:
            self.send_error(404, f"Unknown path: {self.path}")

    def log_message(self, format, *args):
        print(f"HTTP: {format % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)

    print("RIPGuard dashboard server started with dynamic link-cost calculation.")
    print(f"Open http://127.0.0.1:{PORT}/ in your browser.")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDashboard stopped.")
    finally:
        server.server_close()
