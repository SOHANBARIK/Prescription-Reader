import { useSearchParams } from "react-router-dom";

export default function WhereToBuy() {
  const [params] = useSearchParams();
  const name = params.get("name");

  return (
    <div className="card">
      <h2>Where to buy</h2>
      <p className="muted">
        AushadhiSetu does not sell medicines. Use trusted platforms below.
      </p>

      <ul style={{ marginTop: 16 }}>
        <li>
          <a
            href="https://www.google.com/maps/search/Jan+Aushadhi+Kendra+near+me"
            // href="https://janaushadhi.gov.in/StoreLocator"
            target="_blank"
            rel="noreferrer"
          >
            Jan Aushadhi Kendra Near Me
          </a>
        </li>
        <li>
          <a
            href={`https://www.1mg.com/search/all?name=${encodeURIComponent(name)}`}
            target="_blank"
            rel="noreferrer"
          >
            Tata 1mg
          </a>
        </li>
        <li>
          <a
            href={`https://pharmeasy.in/search/all?name=${encodeURIComponent(name)}`}
            target="_blank"
            rel="noreferrer"
          >
            PharmEasy
          </a>
        </li>
        <li>
          <a href={`https://www.google.com/search?q=buy+${encodeURIComponent(name)}`} 
          target="_blank" 
          rel="noreferrer"
          >
            Find at Google</a>
        </li>
      </ul>
    </div>
  );
}
