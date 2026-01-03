import React, { useState } from "react";
import "./DisclaimerModel.css";

const DisclaimerModal = () => {
  const [open, setOpen] = useState(() => {
    return !sessionStorage.getItem("disclaimerAccepted");
  });

  const handleClose = () => {
    sessionStorage.setItem("disclaimerAccepted", "true");
    setOpen(false);
  };

  if (!open) return null;

  return (
    <div className="disclaimer-backdrop">
      <div className="disclaimer-modal">
        <button className="close-btn" onClick={handleClose}>
          ✕
        </button>

        <h2>⚠️ Medical Disclaimer</h2>

        <p>
          AushadhiSetu is an <strong>informational tool</strong> designed to help
          identify medicines and possible generic alternatives using publicly
          available data.
        </p>

        <p>
          This application <strong>does not provide medical advice</strong>.
          Always consult a licensed doctor or pharmacist before changing or
          substituting any medication.
        </p>

        <p>
          Uploaded prescription images are processed temporarily and
          <strong> are not stored</strong>.
        </p>

        <button className="accept-btn" onClick={handleClose}>
          I Understand
        </button>
      </div>
    </div>
  );
};

export default DisclaimerModal;
