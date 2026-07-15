export function ThreadPath() {
  return (
    <div className="thread-layer" aria-hidden="true">
      <svg className="thread-path" viewBox="0 0 100 1000" preserveAspectRatio="none">
        <defs>
          <linearGradient id="thread-story-gradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#bd5a42" />
            <stop offset="42%" stopColor="#2855c7" />
            <stop offset="78%" stopColor="#2855c7" />
            <stop offset="100%" stopColor="#1c8a5c" />
          </linearGradient>
        </defs>
        <path
          className="thread-progress"
          d="M50 0 C20 150 80 250 50 400 S20 650 50 800 S80 950 50 1000"
          pathLength="1"
          stroke="url(#thread-story-gradient)"
        />
      </svg>
    </div>
  );
}
