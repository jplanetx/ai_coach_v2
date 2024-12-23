import React from 'react';

interface Task {
  id: string;
  title: string;
  importance: 'High' | 'Medium' | 'Low';
  urgency: 'High' | 'Medium' | 'Low';
  status: string;
}

interface QuadrantProps {
  title: string;
  tasks: Task[];
  description: string;
  bgColor: string;
}

const Quadrant: React.FC<QuadrantProps> = ({ title, tasks, description, bgColor }) => (
  <div className={`p-4 rounded-lg shadow-lg ${bgColor} h-full flex flex-col`}>
    <h3 className="font-bold text-lg mb-2">{title}</h3>
    <p className="text-sm text-gray-600 mb-4">{description}</p>
    <div className="space-y-2 flex-grow overflow-auto">
      {tasks.map(task => (
        <div 
          key={task.id}
          className="p-3 bg-white rounded-lg shadow hover:shadow-md transition-shadow cursor-move"
        >
          <p className="font-medium">{task.title}</p>
          <div className="flex gap-2 mt-2">
            <span className={`text-xs px-2 py-1 rounded ${
              task.importance === 'High' ? 'bg-red-100 text-red-800' :
              task.importance === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
              'bg-green-100 text-green-800'
            }`}>
              {task.importance}
            </span>
            <span className={`text-xs px-2 py-1 rounded ${
              task.urgency === 'High' ? 'bg-purple-100 text-purple-800' :
              task.urgency === 'Medium' ? 'bg-blue-100 text-blue-800' :
              'bg-gray-100 text-gray-800'
            }`}>
              {task.urgency}
            </span>
            <span className={`text-xs px-2 py-1 rounded bg-gray-100 text-gray-800`}>
              {task.status}
            </span>
          </div>
        </div>
      ))}
      {tasks.length === 0 && (
        <div className="text-center text-gray-500 italic">
          No tasks in this quadrant
        </div>
      )}
    </div>
  </div>
);

interface EisenhowerMatrixProps {
  tasks?: Task[];
}

export const EisenhowerMatrix: React.FC<EisenhowerMatrixProps> = ({ tasks = [] }) => {
  // Helper function to determine if a task is "High" priority
  const isHigh = (value: string) => value === 'High';

  const categorizedTasks = {
    important_urgent: tasks.filter(t => isHigh(t.importance) && isHigh(t.urgency)),
    important_not_urgent: tasks.filter(t => isHigh(t.importance) && !isHigh(t.urgency)),
    not_important_urgent: tasks.filter(t => !isHigh(t.importance) && isHigh(t.urgency)),
    not_important_not_urgent: tasks.filter(t => !isHigh(t.importance) && !isHigh(t.urgency))
  };

  return (
    <div className="grid grid-cols-2 gap-4 p-4 h-[calc(100vh-200px)]">
      <Quadrant
        title="Do First"
        tasks={categorizedTasks.important_urgent}
        description="Important and urgent tasks that need immediate attention"
        bgColor="bg-red-50"
      />
      <Quadrant
        title="Schedule"
        tasks={categorizedTasks.important_not_urgent}
        description="Important but not urgent tasks to plan for later"
        bgColor="bg-blue-50"
      />
      <Quadrant
        title="Delegate or Do Fast"
        tasks={categorizedTasks.not_important_urgent}
        description="Urgent but less important tasks to minimize"
        bgColor="bg-yellow-50"
      />
      <Quadrant
        title="Eliminate or Postpone"
        tasks={categorizedTasks.not_important_not_urgent}
        description="Neither urgent nor important tasks to reconsider"
        bgColor="bg-green-50"
      />
    </div>
  );
};