import { useLocation } from "react-router-dom";
import MedicineCard from "../components/MedicineCard";

export default function Results() {
  const location = useLocation();

  // Prefer router state, fallback to sessionStorage
  const medicines =
    location.state ||
    JSON.parse(sessionStorage.getItem("aushadhi_results")) ||
    [];

  if (!medicines.length) {
    return (
      <div className="card">
        <h3>No medicines detected</h3>
        <p className="muted">
          Upload a clear prescription to see results.
        </p>
      </div>
    );
  }

  return (
    <div>
      <h2>Detected Medicines</h2>

      <div className="results-grid">
        {medicines.map((med, idx) => (
          <MedicineCard key={idx} med={med} />
        ))}
      </div>
    </div>
  );
}
