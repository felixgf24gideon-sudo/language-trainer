import { useState } from 'react';
import TrainingScreen from './components/TrainingScreen';

function App() {
  const [username] = useState('default');

  return (
    <div className="min-h-screen bg-bg-primary text-text-primary font-sans">
      <TrainingScreen username={username} />
    </div>
  );
}

export default App;
