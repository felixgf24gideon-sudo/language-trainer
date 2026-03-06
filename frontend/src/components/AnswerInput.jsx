import { useEffect, useRef } from 'react';

function AnswerInput({ value, onChange, onSubmit, disabled }) {
  const inputRef = useRef(null);

  useEffect(() => {
    if (!disabled && inputRef.current) {
      inputRef.current.focus();
    }
  }, [disabled]);

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !disabled) {
      e.preventDefault();
      onSubmit();
    }
    if (e.key === 'Escape') {
      onChange({ target: { value: '' } });
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-4 px-4">
      <textarea
        ref={inputRef}
        className="answer-input resize-none min-h-[80px]"
        placeholder="Type your answer in English..."
        value={value}
        onChange={onChange}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        rows={3}
        aria-label="Answer input"
      />
      <p className="text-center text-xs text-text-muted mt-2 font-mono">
        Press <span className="text-text-secondary">Enter</span> to submit
        &nbsp;·&nbsp;
        <span className="text-text-secondary">Esc</span> to clear
      </p>
    </div>
  );
}

export default AnswerInput;
