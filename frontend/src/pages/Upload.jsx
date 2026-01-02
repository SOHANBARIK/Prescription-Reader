import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import Loader from "../components/Loader";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default function Upload() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleFile = (e) => {
    const f = e.target.files?.[0];
    if (!f) return;
    setFile(f);
    setPreview(URL.createObjectURL(f));
    setError("");
  };

  const doUpload = async () => {
    if (!file) return setError("Please choose an image first.");
    setLoading(true);
    setError("");
    const form = new FormData();
    form.append("file", file);

    try {
      const res = await axios.post(`${API_BASE_URL}/upload`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      const meds = res.data.medicines || [];
      // persist so results survive hard refresh / navigation
      sessionStorage.setItem("aushadhi_results", JSON.stringify(meds));
      navigate("/results", { state: meds });
    } catch (e) {
      console.error(e);
      setError("Upload failed. Is backend running at http://localhost:5000 ? ");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-page container-grid">
      <section className="upload-left card">
        <h2>Upload Prescription</h2>
        <p className="muted">Take a clear photo of the prescription or upload a scan.</p>

        <label className="dropzone">
          <input type="file" accept="image/*" onChange={handleFile} />
          {!preview && <div className="dz-placeholder">Click or drop image here</div>}
          {preview && <img src={preview} alt="preview" className="preview" />}
        </label>

        <div className="upload-actions">
          <button className="btn btn-primary" onClick={doUpload} disabled={loading}>
            {loading ? "Scanning..." : "Scan Prescription"}
          </button>
          <button className="btn btn-ghost" onClick={() => { setFile(null); setPreview(null); setError(""); }}>
            Reset
          </button>
        </div>

        {loading && <Loader text="Analyzing image with AI..." />}
        {error && <div className="alert error">{error}</div>}
      </section>

      <aside className="upload-right">
        <div className="card">
          <h4>Tips for a clean scan</h4>
          <ul>
            <li>Place prescription on flat surface with good light</li>
            <li>Avoid shadows and reflections</li>
            <li>Capture the entire prescription, not just a portion</li>
          </ul>
        </div>

        <div className="card">
          <h4>Privacy</h4>
          <p className="muted">Images are processed only to detect medicine names — no personal data is stored persistently.</p>
        </div>
      </aside>
    </div>
  );
}
