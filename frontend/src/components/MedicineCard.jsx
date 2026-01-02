export default function MedicineCard({ med }) {
  const alt = med.alternative;
  return (
    <article className="med-card">
      <div className="med-top">
        <h3 className="med-name">{med.detected_name || med.name}</h3>
        <span className={`pill pill-${med.type?.toLowerCase() || "unknown"}`}>
          {med.type || "Unknown"}
        </span>
      </div>

      <div className="med-meta">
        <div className="price">₹{med.price === "N/A" ? "—" : med.price}</div>
        <a className="buy-link" href={med.buy_link} target="_blank" rel="noreferrer">Buy Original →</a>
      </div>

      {alt && (
        <div className="alt-box">
          <div className="alt-title">💡 Cheaper Alternative</div>
          <div className="alt-name">{alt.name}</div>
          <div className="alt-manufacturer">by {alt.manufacturer}</div>
          <div className="alt-savings">Save ₹{Math.round(alt.savings)}</div>
          <a className="alt-buy" href={`https://www.google.com/search?q=buy+${encodeURIComponent(alt.name)}`} target="_blank" rel="noreferrer">Buy Generic</a>
        </div>
      )}
    </article>
  );
}
