export interface Task {
  id: string;
  title: string;
  importance: 'High' | 'Medium' | 'Low';
  urgency: 'High' | 'Medium' | 'Low';
  energy?: 'High' | 'Medium' | 'Low';
  impact?: 'High' | 'Medium' | 'Low';
  effort?: 'High' | 'Medium' | 'Low';
  project?: string;
  goals?: string[];
  blocking?: string[];
  blockedBy?: string[];
  timeEstimate?: number;
}