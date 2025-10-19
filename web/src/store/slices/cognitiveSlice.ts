import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface CognitiveProcess {
  id: string;
  name: string;
  type: 'perception' | 'reasoning' | 'memory' | 'learning' | 'decision' | 'attention' | 'metacognition';
  status: 'active' | 'idle' | 'processing';
  efficiency: number;
  lastActivity: Date;
}

export interface MemoryItem {
  id: string;
  type: 'episodic' | 'semantic' | 'procedural';
  content: string;
  importance: number;
  associations: string[];
  timestamp: Date;
}

export interface CognitiveInsight {
  id: string;
  type: 'pattern' | 'prediction' | 'recommendation' | 'warning';
  title: string;
  description: string;
  confidence: number;
  timestamp: Date;
}

interface CognitiveState {
  processes: CognitiveProcess[];
  memories: MemoryItem[];
  insights: CognitiveInsight[];
  currentFocus: string | null;
  attentionAllocation: Record<string, number>;
  learningMetrics: {
    adaptationRate: number;
    transferEfficiency: number;
    retentionRate: number;
  };
  isMonitoring: boolean;
  error: string | null;
}

const initialState: CognitiveState = {
  processes: [],
  memories: [],
  insights: [],
  currentFocus: null,
  attentionAllocation: {},
  learningMetrics: {
    adaptationRate: 0,
    transferEfficiency: 0,
    retentionRate: 0,
  },
  isMonitoring: false,
  error: null,
};

const cognitiveSlice = createSlice({
  name: 'cognitive',
  initialState,
  reducers: {
    setProcesses: (state, action: PayloadAction<CognitiveProcess[]>) => {
      state.processes = action.payload;
    },
    updateProcess: (state, action: PayloadAction<CognitiveProcess>) => {
      const index = state.processes.findIndex(process => process.id === action.payload.id);
      if (index !== -1) {
        state.processes[index] = action.payload;
      }
    },
    addMemory: (state, action: PayloadAction<MemoryItem>) => {
      state.memories.push(action.payload);
    },
    addInsight: (state, action: PayloadAction<CognitiveInsight>) => {
      state.insights.push(action.payload);
    },
    setCurrentFocus: (state, action: PayloadAction<string | null>) => {
      state.currentFocus = action.payload;
    },
    updateAttentionAllocation: (state, action: PayloadAction<Record<string, number>>) => {
      state.attentionAllocation = action.payload;
    },
    updateLearningMetrics: (state, action: PayloadAction<Partial<CognitiveState['learningMetrics']>>) => {
      state.learningMetrics = { ...state.learningMetrics, ...action.payload };
    },
    setMonitoring: (state, action: PayloadAction<boolean>) => {
      state.isMonitoring = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const {
  setProcesses,
  updateProcess,
  addMemory,
  addInsight,
  setCurrentFocus,
  updateAttentionAllocation,
  updateLearningMetrics,
  setMonitoring,
  setError,
} = cognitiveSlice.actions;

export default cognitiveSlice.reducer;