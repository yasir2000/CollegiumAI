import { configureStore } from '@reduxjs/toolkit';
import authReducer from './features/auth/authSlice';
import agentReducer from './features/agents/agentSlice';
import blockchainReducer from './features/blockchain/blockchainSlice';
import governanceReducer from './features/governance/governanceSlice';
import universityReducer from './features/university/universitySlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    agents: agentReducer,
    blockchain: blockchainReducer,
    governance: governanceReducer,
    university: universityReducer,
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