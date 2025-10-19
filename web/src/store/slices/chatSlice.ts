import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  timestamp: Date;
  confidence?: number;
  cognitiveInsights?: string[];
  agentInfo?: {
    name: string;
    type: string;
  };
}

interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  activeConversationId: string | null;
}

const initialState: ChatState = {
  messages: [],
  isLoading: false,
  error: null,
  activeConversationId: null,
};

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addMessage: (state, action: PayloadAction<ChatMessage>) => {
      state.messages.push(action.payload);
    },
    setMessages: (state, action: PayloadAction<ChatMessage[]>) => {
      state.messages = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    clearChat: (state) => {
      state.messages = [];
      state.error = null;
    },
    setActiveConversation: (state, action: PayloadAction<string | null>) => {
      state.activeConversationId = action.payload;
    },
  },
});

export const { 
  addMessage, 
  setMessages, 
  setLoading, 
  setError, 
  clearChat,
  setActiveConversation 
} = chatSlice.actions;

export default chatSlice.reducer;