import { useLocation } from "react-router-dom";
import MedicineCard from "../components/MedicineCard";

export default function Results() {
  const loc = useLocation();
  // prefer state from navigation, fallback to session storage (survives refresh)
  const navState = loc.state;
  const persisted = typeof window !== "undefined" && sessionStorage.getItem("aushadhi_results");
  const items = navState || (persisted ? JSON.parse(persisted) : []);

  return (
    <div className="results-page container-grid">
      <section className="results-left">
        <h2>Detected Medicines</h2>
        <p className="muted">Review detected medicines and suggested generic alternatives.</p>

        {(!items || items.length === 0) && (
          <div className="card empty">No results yet. Upload a prescription to get started.</div>
        )}

        <div className="results-grid">
          {items.map((med, i) => (
            <MedicineCard key={i} med={med} />
          ))}
        </div>
      </section>

      <aside className="results-right">
        <div className="card">
          <h4>How to interpret results</h4>
          <p className="muted">Green boxes indicate cheaper generic alternatives found in the database.</p>
        </div>

        <div className="card">
          <h4>Next steps</h4>
          <ol>
            <li>Check the alternative's manufacturer and price.</li>
            <li>Confirm with a pharmacist before substituting prescribed brand.</li>
            <li>Order from a trusted source or visit a Jan Aushadhi store.</li>
          </ol>
        </div>
      </aside>
    </div>
  );
}
