import { useEffect, useRef } from 'react';

function ScoreRow({ label, score, max = 5 }) {
  const pct = Math.round((score / max) * 100);
  const filled = score >= 4 ? 'bg-accent-success' : score >= 3 ? 'bg-accent-warning' : 'bg-accent-error';

  return (
    <div className="flex items-center gap-3 text-sm">
      <span className="w-36 text-text-secondary text-right">{label}</span>
      <div className="score-bar flex-1">
        <div
          className={`score-fill ${filled}`}
          style={{ width: `${pct}%` }}
          role="progressbar"
          aria-valuenow={score}
          aria-valuemin={0}
          aria-valuemax={max}
        />
      </div>
      <span className="w-10 text-text-primary font-mono text-xs">
        {score}/{max}
      </span>
    </div>
  );
}

function FeedbackCard({ evaluation, isCorrect, onNext }) {
  const nextBtnRef = useRef(null);

  useEffect(() => {
    const handleKey = (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        onNext();
      }
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [onNext]);

  useEffect(() => {
    if (nextBtnRef.current) {
      nextBtnRef.current.focus();
    }
  }, []);

  if (!evaluation) return null;

  const { scores, errors, feedback } = evaluation;
  const avg = scores?.average ?? 0;
  const avgPct = Math.round((avg / 5) * 100);

  return (
    <div
      className={`max-w-2xl mx-auto mt-6 px-4 rounded-lg p-6 border-2 transition-all duration-300 ${
        isCorrect ? 'border-accent-success bg-bg-secondary' : 'border-accent-error bg-bg-secondary'
      }`}
    >
      {/* Status */}
      <div className="flex items-center gap-2 mb-5">
        <span className={`text-2xl font-bold ${isCorrect ? 'text-accent-success' : 'text-accent-error'}`}>
          {isCorrect ? '✓ Sempurna!' : '✗ Ada kesalahan'}
        </span>
      </div>

      {/* Scores */}
      {scores && (
        <div className="mb-5">
          <p className="text-xs text-text-muted uppercase tracking-widest mb-3 font-mono">📊 Scores</p>
          <div className="space-y-2">
            <ScoreRow label="Grammar" score={scores.grammar} />
            <ScoreRow label="Vocabulary" score={scores.vocabulary} />
            <ScoreRow label="Naturalness" score={scores.naturalness} />
            <ScoreRow label="Task Completion" score={scores.task_completion} />
          </div>
          <p className="text-right text-sm text-text-secondary mt-3 font-mono">
            Average:{' '}
            <span className="text-text-primary font-semibold">
              {avg.toFixed(1)}/5 ({avgPct}%)
            </span>
          </p>
        </div>
      )}

      {/* Errors */}
      {errors && errors.length > 0 && (
        <div className="mb-4">
          <p className="text-xs text-text-muted uppercase tracking-widest mb-2 font-mono">Errors</p>
          <ul className="space-y-1">
            {errors.map((err, i) => (
              <li key={i} className="text-sm text-accent-error flex gap-2">
                <span>•</span>
                <span>{err}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Correction */}
      {feedback?.correction && (
        <div className="mb-4">
          <p className="text-xs text-text-muted uppercase tracking-widest mb-1 font-mono">Koreksi</p>
          <p className="text-sm text-text-primary bg-bg-tertiary rounded px-3 py-2 font-mono">
            {feedback.correction}
          </p>
        </div>
      )}

      {/* Explanation */}
      {feedback?.explanation && (
        <div className="mb-4">
          <p className="text-xs text-text-muted uppercase tracking-widest mb-1 font-mono">Penjelasan</p>
          <p className="text-sm text-text-secondary leading-relaxed">{feedback.explanation}</p>
        </div>
      )}

      {/* Better examples */}
      {feedback?.better_examples && feedback.better_examples.length > 0 && (
        <div className="mb-4">
          <p className="text-xs text-text-muted uppercase tracking-widest mb-1 font-mono">
            Contoh yang lebih baik
          </p>
          <ul className="space-y-1">
            {feedback.better_examples.map((ex, i) => (
              <li key={i} className="text-sm text-text-secondary font-mono bg-bg-tertiary rounded px-3 py-1">
                {ex}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Next button */}
      <div className="flex items-center justify-center gap-3 mt-6">
        <button
          ref={nextBtnRef}
          className="btn-primary"
          onClick={onNext}
          aria-label="Next task"
        >
          Next Task
        </button>
        <span className="text-xs text-text-muted font-mono">or Press Enter</span>
      </div>
    </div>
  );
}

export default FeedbackCard;
