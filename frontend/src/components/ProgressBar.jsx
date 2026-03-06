function ProgressBar({ level = 1, streak = 0, accuracy = 0 }) {
  const accuracyPct = Math.round(accuracy * 100);

  return (
    <div className="w-full bg-bg-secondary border-b border-bg-tertiary py-3 px-6">
      <div className="max-w-2xl mx-auto flex items-center justify-center gap-6 text-sm text-text-secondary font-mono">
        <span>
          Level <span className="text-text-primary font-semibold">{level}</span>
        </span>
        <span className="text-bg-tertiary">|</span>
        <span>
          Streak:{' '}
          <span className="text-accent-warning font-semibold">
            {streak} {streak > 0 ? '🔥' : ''}
          </span>
        </span>
        <span className="text-bg-tertiary">|</span>
        <span>
          Accuracy:{' '}
          <span className="text-text-primary font-semibold">{accuracyPct}%</span>
        </span>
      </div>
    </div>
  );
}

export default ProgressBar;
