import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface AgentMessage {
  id: string;
  type: 'user' | 'agent' | 'system';
  content: string;
  timestamp: Date;
  agentType?: string;
  metadata?: any;
}

export interface AgentSession {
  id: string;
  agentType: string;
  title: string;
  messages: AgentMessage[];
  isActive: boolean;
  createdAt: Date;
  lastActivity: Date;
}

export interface AgentState {
  sessions: AgentSession[];
  activeSessionId: string | null;
  availableAgents: string[];
  isLoading: boolean;
  error: string | null;
}

const initialState: AgentState = {
  sessions: [],
  activeSessionId: null,
  availableAgents: [
    'academic_advisor',
    'student_services',
    'bologna_process',
    'admissions',
    'financial_aid',
    'career_services',
  ],
  isLoading: false,
  error: null,
};

const agentSlice = createSlice({
  name: 'agents',
  initialState,
  reducers: {
    createSession: (state, action: PayloadAction<{ agentType: string; title: string }>) => {
      const newSession: AgentSession = {
        id: Date.now().toString(),
        agentType: action.payload.agentType,
        title: action.payload.title,
        messages: [],
        isActive: true,
        createdAt: new Date(),
        lastActivity: new Date(),
      };
      state.sessions.push(newSession);
      state.activeSessionId = newSession.id;
    },
    
    setActiveSession: (state, action: PayloadAction<string>) => {
      state.activeSessionId = action.payload;
    },
    
    addMessage: (state, action: PayloadAction<{ sessionId: string; message: Omit<AgentMessage, 'id'> }>) => {
      const session = state.sessions.find(s => s.id === action.payload.sessionId);
      if (session) {
        const newMessage: AgentMessage = {
          ...action.payload.message,
          id: Date.now().toString(),
        };
        session.messages.push(newMessage);
        session.lastActivity = new Date();
      }
    },
    
    updateMessage: (state, action: PayloadAction<{ sessionId: string; messageId: string; content: string }>) => {
      const session = state.sessions.find(s => s.id === action.payload.sessionId);
      if (session) {
        const message = session.messages.find(m => m.id === action.payload.messageId);
        if (message) {
          message.content = action.payload.content;
        }
      }
    },
    
    deleteSession: (state, action: PayloadAction<string>) => {
      state.sessions = state.sessions.filter(s => s.id !== action.payload);
      if (state.activeSessionId === action.payload) {
        state.activeSessionId = state.sessions.length > 0 ? state.sessions[0].id : null;
      }
    },
    
    clearError: (state) => {
      state.error = null;
    },
    
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.isLoading = false;
    },
  },
});

export const {
  createSession,
  setActiveSession,
  addMessage,
  updateMessage,
  deleteSession,
  clearError,
  setLoading,
  setError,
} = agentSlice.actions;

export default agentSlice.reducer;