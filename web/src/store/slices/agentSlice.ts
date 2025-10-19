import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface Agent {
  id: string;
  name: string;
  type: string;
  status: 'active' | 'idle' | 'busy' | 'offline';
  expertise: string[];
  currentTask?: string;
  performance: {
    efficiency: number;
    accuracy: number;
    collaborationScore: number;
  };
}

export interface TaskAssignment {
  id: string;
  description: string;
  assignedAgents: string[];
  status: 'pending' | 'in-progress' | 'completed' | 'failed';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  createdAt: Date;
  completedAt?: Date;
}

interface AgentState {
  agents: Agent[];
  tasks: TaskAssignment[];
  activeCollaboration: boolean;
  collaborationMetrics: {
    activeTasks: number;
    completedTasks: number;
    averageCompletionTime: number;
    successRate: number;
  };
  isLoading: boolean;
  error: string | null;
}

const initialState: AgentState = {
  agents: [],
  tasks: [],
  activeCollaboration: false,
  collaborationMetrics: {
    activeTasks: 0,
    completedTasks: 0,
    averageCompletionTime: 0,
    successRate: 0,
  },
  isLoading: false,
  error: null,
};

const agentSlice = createSlice({
  name: 'agent',
  initialState,
  reducers: {
    setAgents: (state, action: PayloadAction<Agent[]>) => {
      state.agents = action.payload;
    },
    updateAgent: (state, action: PayloadAction<Agent>) => {
      const index = state.agents.findIndex(agent => agent.id === action.payload.id);
      if (index !== -1) {
        state.agents[index] = action.payload;
      }
    },
    addTask: (state, action: PayloadAction<TaskAssignment>) => {
      state.tasks.push(action.payload);
    },
    updateTask: (state, action: PayloadAction<TaskAssignment>) => {
      const index = state.tasks.findIndex(task => task.id === action.payload.id);
      if (index !== -1) {
        state.tasks[index] = action.payload;
      }
    },
    setActiveCollaboration: (state, action: PayloadAction<boolean>) => {
      state.activeCollaboration = action.payload;
    },
    updateCollaborationMetrics: (state, action: PayloadAction<Partial<AgentState['collaborationMetrics']>>) => {
      state.collaborationMetrics = { ...state.collaborationMetrics, ...action.payload };
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const {
  setAgents,
  updateAgent,
  addTask,
  updateTask,
  setActiveCollaboration,
  updateCollaborationMetrics,
  setLoading,
  setError,
} = agentSlice.actions;

export default agentSlice.reducer;