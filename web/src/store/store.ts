import { configureStore } from '@reduxjs/toolkit';
import personaSlice from './slices/personaSlice';
import chatSlice from './slices/chatSlice';
import agentSlice from './slices/agentSlice';
import cognitiveSlice from './slices/cognitiveSlice';
import systemSlice from './slices/systemSlice';

// Create simple slices to prevent errors
const blockchainSlice = {
  name: 'blockchain',
  reducer: (state = { isConnected: false, networkId: null, blockNumber: null, credentials: [], isLoading: false, error: null }, action: any) => state
};

const authSlice = {
  name: 'auth',
  reducer: (state = { user: null, isAuthenticated: false, isLoading: false, error: null }, action: any) => state
};

export const store = configureStore({
  reducer: {
    persona: personaSlice,
    chat: chatSlice,
    agent: agentSlice,
    cognitive: cognitiveSlice,
    system: systemSlice,
    blockchain: blockchainSlice.reducer,
    auth: authSlice.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST'],
      },
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;