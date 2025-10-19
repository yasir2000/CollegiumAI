import { configureStore } from '@reduxjs/toolkit';
import personaSlice from './slices/personaSlice';
import chatSlice from './slices/chatSlice';
import agentSlice from './slices/agentSlice';
import cognitiveSlice from './slices/cognitiveSlice';
import systemSlice from './slices/systemSlice';

export const store = configureStore({
  reducer: {
    persona: personaSlice,
    chat: chatSlice,
    agent: agentSlice,
    cognitive: cognitiveSlice,
    system: systemSlice,
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