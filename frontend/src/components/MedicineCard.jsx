export default function MedicineCard({ med }) {
  const alt = med.alternative;

  const price =
    typeof med.price === "number" && med.price > 0 ? med.price : null;

  const savings =
    alt && typeof alt.savings === "number" ? Math.round(alt.savings) : null;

  const percent =
    price && savings ? Math.round((savings / price) * 100) : null;

  return (
    <article className="med-card">
      {/* Top */}
      <div className="med-top">
        <h3 className="med-name">
          {med.detected_name || med.name || "Unknown Medicine"}
        </h3>

        <span className={`pill pill-${med.type?.toLowerCase() || "unknown"}`}>
          {med.type || "Unknown"}
        </span>
      </div>

      {/* Price + Buy */}
      <div className="med-meta">
        <div className="price">
          {price ? `₹${price}` : "Price not available"}
        </div>
        <a className="buy-link" 
        href={`/where-to-buy?name=${encodeURIComponent(med.detected_name)}`}
        >Where to buy →</a>
        </div>

      {/* Alternative */}
      {alt && savings && (
        <div className="alt-box">
          <div className="alt-title">💡 Cheaper Alternative</div>

          <div className="alt-name">{alt.name}</div>
          <div className="alt-manufacturer">by {alt.manufacturer}</div>

          <div className="alt-savings">
            Save ₹{savings}
            {percent && <span> ({percent}% cheaper)</span>}
          </div>

          <a
            className="alt-buy"
            href="https://janaushadhi.gov.in/StoreLocator"
            target="_blank"
            rel="noreferrer"
          >
            Buy at Jan Aushadhi →
          </a>
        </div>
      )}
    </article>
  );
}