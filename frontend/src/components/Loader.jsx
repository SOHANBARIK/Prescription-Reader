export default function Loader({ text = "Processing..." }) {
  return (
    <div className="loader-wrap">
      <div className="spinner" />
      <div className="loader-text">{text}</div>
    </div>
  );
}
