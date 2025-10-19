import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface PersonaType {
  id: string;
  name: string;
  type: 'student' | 'faculty' | 'staff';
  category: string;
  description: string;
  cognitiveProfile: {
    attentionParams: Record<string, number>;
    learningParams: Record<string, number>;
    decisionParams: Record<string, number>;
  };
  capabilities: string[];
  supportAreas: string[];
}

interface PersonaState {
  currentPersona: PersonaType | null;
  availablePersonas: PersonaType[];
  isLoading: boolean;
  error: string | null;
}

const initialState: PersonaState = {
  currentPersona: null,
  availablePersonas: [],
  isLoading: false,
  error: null,
};

const personaSlice = createSlice({
  name: 'persona',
  initialState,
  reducers: {
    setCurrentPersona: (state, action: PayloadAction<PersonaType>) => {
      state.currentPersona = action.payload;
    },
    setAvailablePersonas: (state, action: PayloadAction<PersonaType[]>) => {
      state.availablePersonas = action.payload;
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.isLoading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const { setCurrentPersona, setAvailablePersonas, setLoading, setError } = personaSlice.actions;
export default personaSlice.reducer;