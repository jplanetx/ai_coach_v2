export interface Task {
  id: string;
  title: string;
  importance: 'High' | 'Medium' | 'Low';
  urgency: 'High' | 'Medium' | 'Low';
  status: string;
}