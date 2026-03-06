function TaskCard({ instruction, taskType }) {
  const typeLabel = {
    word_translation: 'Word Translation',
    phrase_translation: 'Phrase Translation',
    sentence_translation: 'Sentence Translation',
    constrained_production: 'Constrained Production',
    context_production: 'Context Production',
    paragraph_production: 'Paragraph Production',
  }[taskType] || taskType;

  return (
    <div className="task-card">
      {taskType && (
        <p className="text-xs text-text-muted uppercase tracking-widest mb-4 font-mono">
          {typeLabel}
        </p>
      )}
      <p className="text-xl text-text-primary leading-relaxed">{instruction}</p>
    </div>
  );
}

export default TaskCard;
