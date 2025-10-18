import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface Credential {
  id: number;
  studentAddress: string;
  title: string;
  program: string;
  issueDate: Date;
  verified: boolean;
  governanceFrameworks: string[];
  bolognaData?: {
    ectsCredits: number;
    eqfLevel: number;
    diplomaSupplementIssued: boolean;
  };
}

export interface BlockchainState {
  isConnected: boolean;
  networkId: number | null;
  blockNumber: number | null;
  credentials: Credential[];
  isLoading: boolean;
  error: string | null;
}

const initialState: BlockchainState = {
  isConnected: false,
  networkId: null,
  blockNumber: null,
  credentials: [],
  isLoading: false,
  error: null,
};

const blockchainSlice = createSlice({
  name: 'blockchain',
  initialState,
  reducers: {
    setConnectionStatus: (state, action: PayloadAction<boolean>) => {
      state.isConnected = action.payload;
    },
    setNetworkInfo: (state, action: PayloadAction<{ networkId: number; blockNumber: number }>) => {
      state.networkId = action.payload.networkId;
      state.blockNumber = action.payload.blockNumber;
    },
    setCredentials: (state, action: PayloadAction<Credential[]>) => {
      state.credentials = action.payload;
    },
    addCredential: (state, action: PayloadAction<Credential>) => {
      state.credentials.push(action.payload);
    },
    updateCredential: (state, action: PayloadAction<Credential>) => {
      const index = state.credentials.findIndex(c => c.id === action.payload.id);
      if (index !== -1) {
        state.credentials[index] = action.payload;
      }
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
  setConnectionStatus,
  setNetworkInfo,
  setCredentials,
  addCredential,
  updateCredential,
  setLoading,
  setError,
} = blockchainSlice.actions;

export default blockchainSlice.reducer;