export function ThreadPath() {
  return (
    <div className="thread-layer" aria-hidden="true">
      <svg className="thread-path" viewBox="0 0 100 1000" preserveAspectRatio="none">
        <path
          className="thread-progress"
          d="M50 0 C20 150 80 250 50 400 S20 650 50 800 S80 950 50 1000"
          pathLength="1"
        />
      </svg>
    </div>
  );
}
