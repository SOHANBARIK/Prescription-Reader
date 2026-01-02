import { useNavigate } from "react-router-dom";
import logo from "../assets/logo.png";

export default function Home() {
  const nav = useNavigate();
  return (
    <div className="home-hero">
      <div className="hero-card">
        <img src={logo} alt="AushadhiSetu" className="hero-logo" />
        <h1>Scan Prescriptions. Save Money.</h1>
        <p className="hero-sub">
          AI-powered medicine recognition and Jan Aushadhi alternatives — fast, reliable, and low-cost.
        </p>

        <div className="hero-features">
          <div>💊 Genuine Medicines</div>
          <div>💰 Affordable Alternatives</div>
          <div>📸 Upload Prescriptions</div>
        </div>

        <div className="hero-actions">
          <button className="btn btn-primary" onClick={() => nav("/upload")}>Upload Prescription 📸</button>
          <button className="btn btn-outline" onClick={() => nav("/about")}>Learn More</button>
        </div>
      </div>

      <aside className="hero-side">
        <div className="side-card">
          <h4>Why AushadhiSetu?</h4>
          <ul>
            <li>Brings Jan Aushadhi alternatives to patients</li>
            <li>Transparent price comparisons</li>
            <li>Easy to use — no pharmacy visits required</li>
          </ul>
        </div>
      </aside>
    </div>
  );
}
