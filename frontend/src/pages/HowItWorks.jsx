import React from "react";

const HowItWorks = () => {
  return (
    <div style={{ maxWidth: "720px", margin: "2rem auto", padding: "0 1rem" }}>
      <h1>How AushadhiSetu Works</h1>

      <ol style={{ lineHeight: "1.8", marginTop: "1rem" }}>
        <li>
          You upload a photo of a valid medical prescription or search a medicine name.
        </li>
        <li>
          The system reads medicine names using OCR and matches them against a public
          medicine database.
        </li>
        <li>
          We compare branded medicines with available lower-cost generic alternatives.
        </li>
        <li>
          You see indicative prices and guidance on how to find these medicines locally.
        </li>
      </ol>

      <p style={{ marginTop: "1.5rem", color: "#374151" }}>
        AushadhiSetu does not sell medicines and does not provide medical advice.
        All information is intended to help users make informed discussions
        with doctors or pharmacists.
      </p>
    </div>
  );
};

export default HowItWorks;
