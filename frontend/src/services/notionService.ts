import { Task } from '../types';

const API_BASE_URL = 'http://localhost:8000';

export const fetchTasks = async (): Promise<Task[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/tasks`);
    if (!response.ok) {
      throw new Error('Failed to fetch tasks');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching tasks:', error);
    throw error;
  }
};

export const updateTaskProperties = async (taskId: string, properties: Record<string, any>): Promise<void> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}/properties`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(properties),
    });
    if (!response.ok) {
      throw new Error('Failed to update task');
    }
  } catch (error) {
    console.error('Error updating task:', error);
    throw error;
  }
};