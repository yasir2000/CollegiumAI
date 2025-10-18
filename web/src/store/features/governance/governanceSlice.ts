import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface ComplianceAudit {
  id: number;
  institution: string;
  framework: string;
  auditArea: string;
  status: 'compliant' | 'non_compliant' | 'under_review';
  findings: string;
  recommendations: string;
  nextReviewDate: Date;
  createdAt: Date;
}

export interface GovernanceState {
  audits: ComplianceAudit[];
  activeFrameworks: string[];
  complianceStatus: Record<string, 'compliant' | 'non_compliant' | 'under_review'>;
  isLoading: boolean;
  error: string | null;
}

const initialState: GovernanceState = {
  audits: [],
  activeFrameworks: ['AACSB', 'HEFCE', 'WASC', 'BOLOGNA_PROCESS'],
  complianceStatus: {},
  isLoading: false,
  error: null,
};

const governanceSlice = createSlice({
  name: 'governance',
  initialState,
  reducers: {
    setAudits: (state, action: PayloadAction<ComplianceAudit[]>) => {
      state.audits = action.payload;
    },
    addAudit: (state, action: PayloadAction<ComplianceAudit>) => {
      state.audits.push(action.payload);
    },
    updateAudit: (state, action: PayloadAction<ComplianceAudit>) => {
      const index = state.audits.findIndex(a => a.id === action.payload.id);
      if (index !== -1) {
        state.audits[index] = action.payload;
      }
    },
    setComplianceStatus: (state, action: PayloadAction<Record<string, 'compliant' | 'non_compliant' | 'under_review'>>) => {
      state.complianceStatus = action.payload;
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
  setAudits,
  addAudit,
  updateAudit,
  setComplianceStatus,
  setLoading,
  setError,
} = governanceSlice.actions;

export default governanceSlice.reducer;