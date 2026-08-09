export default function LoadingState({ message }) {
  return (
    <div className="loading-state">
      <div className="spinner" />
      <span>{message}</span>
    </div>
  );
}
