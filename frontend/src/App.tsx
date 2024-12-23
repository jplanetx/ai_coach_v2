import React, { useEffect, useState } from 'react';
import { EisenhowerMatrix } from './components/EisenhowerMatrix';
import { fetchTasks } from './services/notionService';
import type { Task } from './types';

const App: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      // Only show loading state if we don't have any tasks yet
      if (tasks.length === 0) {
        setLoading(true);
      }
      const fetchedTasks = await fetchTasks();
      setTasks(fetchedTasks);
      setLastUpdated(new Date());
      setError(null);
    } catch (err) {
      setError('Failed to load tasks. Please try again.');
      console.error('Error loading tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                AI Coach
              </h1>
              <p className="mt-1 text-sm text-gray-500">
                Viewing {tasks.length} active tasks from Notion
                {lastUpdated && ` • Last updated ${lastUpdated.toLocaleTimeString()}`}
              </p>
            </div>
            <button
              onClick={loadTasks}
              disabled={loading}
              className={`px-4 py-2 rounded-lg text-sm font-medium ${
                loading
                  ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  : 'bg-blue-50 text-blue-600 hover:bg-blue-100'
              }`}
            >
              {loading ? 'Loading...' : 'Refresh Tasks'}
            </button>
          </div>
        </div>
      </header>
      <main className="max-w-7xl mx-auto py-6 px-4">
        {loading && tasks.length === 0 ? (
          <div className="flex justify-center items-center h-64">
            <p className="text-lg text-gray-600">Loading tasks...</p>
          </div>
        ) : error ? (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-800">{error}</p>
            <button 
              onClick={loadTasks}
              className="mt-2 px-4 py-2 bg-red-100 text-red-800 rounded hover:bg-red-200"
            >
              Retry
            </button>
          </div>
        ) : (
          <div className={loading ? 'opacity-50' : ''}>
            <EisenhowerMatrix tasks={tasks} />
          </div>
        )}
      </main>
    </div>
  );
};

export default App;