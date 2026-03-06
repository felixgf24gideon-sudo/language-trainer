import { useState, useEffect, useCallback } from 'react';
import ProgressBar from './ProgressBar';
import TaskCard from './TaskCard';
import AnswerInput from './AnswerInput';
import FeedbackCard from './FeedbackCard';
import { generateTask, evaluateAnswer, getUserStats } from '../services/api';

function TrainingScreen({ username }) {
  const [currentTask, setCurrentTask] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [evaluation, setEvaluation] = useState(null);
  const [isLoadingTask, setIsLoadingTask] = useState(false);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [stats, setStats] = useState({ level: 1, streak: 0, accuracy: 0 });
  const [error, setError] = useState(null);

  const fetchStats = useCallback(async () => {
    try {
      const data = await getUserStats(username);
      setStats({
        level: data.level,
        streak: data.streak,
        accuracy: data.accuracy,
      });
    } catch {
      // stats are non-critical; silently ignore
    }
  }, [username]);

  const fetchTask = useCallback(async () => {
    setIsLoadingTask(true);
    setError(null);
    setEvaluation(null);
    setUserAnswer('');
    try {
      const task = await generateTask(username);
      setCurrentTask(task);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to load task. Please try again.');
    } finally {
      setIsLoadingTask(false);
    }
  }, [username]);

  // Load first task on mount
  useEffect(() => {
    fetchTask();
    fetchStats();
  }, [fetchTask, fetchStats]);

  const handleSubmit = async () => {
    if (!userAnswer.trim() || !currentTask || isEvaluating) return;

    setIsEvaluating(true);
    setError(null);
    try {
      const result = await evaluateAnswer(currentTask.task_id, userAnswer);
      setEvaluation(result);
      await fetchStats();
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to evaluate answer. Please try again.');
    } finally {
      setIsEvaluating(false);
    }
  };

  const handleNext = useCallback(() => {
    fetchTask();
    fetchStats();
  }, [fetchTask, fetchStats]);

  // Ctrl/Cmd+R to restart session
  useEffect(() => {
    const handleKey = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'r' && !evaluation) {
        e.preventDefault();
        fetchTask();
      }
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [evaluation, fetchTask]);

  return (
    <div className="flex flex-col min-h-screen">
      <ProgressBar
        level={stats.level}
        streak={stats.streak}
        accuracy={stats.accuracy}
      />

      <main className="flex-1 flex flex-col justify-center py-10 px-4">
        {/* Loading task */}
        {isLoadingTask && (
          <div className="text-center text-text-muted font-mono animate-pulse">
            Loading task...
          </div>
        )}

        {/* Error state */}
        {error && !isLoadingTask && (
          <div className="max-w-2xl mx-auto text-center">
            <p className="text-accent-error mb-4">{error}</p>
            <button className="btn-primary" onClick={fetchTask}>
              Retry
            </button>
          </div>
        )}

        {/* Task display */}
        {!isLoadingTask && currentTask && !error && (
          <>
            <TaskCard
              instruction={currentTask.instruction}
              taskType={currentTask.task_type}
            />

            {/* Answer input – hidden after evaluation */}
            {!evaluation && (
              <AnswerInput
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                onSubmit={handleSubmit}
                disabled={isEvaluating}
              />
            )}

            {/* Evaluating indicator */}
            {isEvaluating && (
              <p className="text-center text-text-muted font-mono mt-4 animate-pulse">
                Evaluating...
              </p>
            )}

            {/* Feedback */}
            {evaluation && !isEvaluating && (
              <FeedbackCard
                evaluation={evaluation}
                isCorrect={evaluation.is_correct}
                onNext={handleNext}
              />
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default TrainingScreen;
