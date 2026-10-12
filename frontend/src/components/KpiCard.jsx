export function KpiCard({ label, value, helper, tone = "neutral" }) {
  return (
    <section className={`kpi-card ${tone}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{helper}</small>
    </section>
  );
}
