import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { AlertTriangle, Boxes, Clock, PackageCheck, Truck } from "lucide-react";
import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { KpiCard } from "./components/KpiCard";
import { getJson } from "./lib/api";
import "./styles.css";

function pct(value) {
  return value == null ? "-" : `${(Number(value) * 100).toFixed(1)}%`;
}

function money(value) {
  return new Intl.NumberFormat("en-ZA", {
    style: "currency",
    currency: "ZAR",
    maximumFractionDigits: 0
  }).format(Number(value || 0));
}

function App() {
  const [state, setState] = useState({
    kpis: null,
    suppliers: [],
    productRegion: [],
    recommendations: [],
    loading: true,
    error: null
  });

  useEffect(() => {
    Promise.all([
      getJson("/kpis"),
      getJson("/suppliers"),
      getJson("/product-region"),
      getJson("/recommendations")
    ])
      .then(([kpis, suppliers, productRegion, recommendations]) => {
        setState({ kpis, suppliers, productRegion, recommendations, loading: false, error: null });
      })
      .catch((error) => setState((current) => ({ ...current, loading: false, error: error.message })));
  }, []);

  const worstBottlenecks = useMemo(() => state.productRegion.slice(0, 8), [state.productRegion]);

  if (state.loading) {
    return <main className="page"><div className="status">Loading operations dashboard...</div></main>;
  }

  if (state.error) {
    return <main className="page"><div className="status error">API error: {state.error}</div></main>;
  }

  return (
    <main className="page">
      <header className="topbar">
        <div>
          <p>Operations intelligence</p>
          <h1>Inventory, Fulfilment & Supplier Performance</h1>
        </div>
        <div className="health"><PackageCheck size={18} /> SQL views powering BI-ready metrics</div>
      </header>

      <section className="kpi-grid">
        <KpiCard label="Service Level" value={pct(state.kpis.service_level)} helper="Fulfilled units / ordered units" tone="green" />
        <KpiCard label="On-Time Delivery" value={pct(state.kpis.on_time_delivery_rate)} helper="Supplier orders delivered on plan" tone="blue" />
        <KpiCard label="Stockout Rate" value={pct(state.kpis.stockout_rate)} helper="Order lines with availability failure" tone="red" />
        <KpiCard label="Avg Lead Time" value={`${Number(state.kpis.average_lead_time_days || 0).toFixed(1)} days`} helper="Order to actual delivery" />
        <KpiCard label="Operational Cost" value={money(state.kpis.operational_cost)} helper="Freight, transport, holding cost" />
        <KpiCard label="Delayed Orders" value={state.kpis.delayed_orders || 0} helper="Late purchase order count" tone="amber" />
      </section>

      <section className="dashboard-grid">
        <div className="panel wide">
          <div className="panel-title"><Truck size={18} /> Supplier reliability</div>
          <ResponsiveContainer width="100%" height={310}>
            <BarChart data={state.suppliers}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="supplier_name" tick={{ fontSize: 12 }} />
              <YAxis tickFormatter={(v) => `${v * 100}%`} />
              <Tooltip formatter={(value) => pct(value)} />
              <Legend />
              <Bar dataKey="on_time_delivery_rate" name="On-time delivery" fill="#2f80ed" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="panel">
          <div className="panel-title"><AlertTriangle size={18} /> Bottleneck drill-down</div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Region</th>
                  <th>Stockout</th>
                  <th>Turnover</th>
                </tr>
              </thead>
              <tbody>
                {worstBottlenecks.map((row) => (
                  <tr key={`${row.product_name}-${row.region_name}`}>
                    <td>{row.product_name}</td>
                    <td>{row.region_name}</td>
                    <td>{pct(row.stockout_rate)}</td>
                    <td>{row.inventory_turnover ?? "-"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="panel">
          <div className="panel-title"><Clock size={18} /> Supplier lead times</div>
          <div className="supplier-list">
            {state.suppliers.map((supplier) => (
              <div className="supplier-row" key={supplier.supplier_name}>
                <div>
                  <strong>{supplier.supplier_name}</strong>
                  <span>{supplier.category} / {supplier.risk_tier} risk</span>
                </div>
                <b>{Number(supplier.average_lead_time_days).toFixed(1)}d</b>
              </div>
            ))}
          </div>
        </div>

        <div className="panel wide">
          <div className="panel-title"><Boxes size={18} /> Process improvement recommendations</div>
          <div className="recommendations">
            {state.recommendations.map((item) => (
              <article key={`${item.focus_area}-${item.insight}`}>
                <span>{item.priority}</span>
                <h3>{item.focus_area}</h3>
                <p>{item.insight}</p>
                <small>{item.action}</small>
              </article>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
