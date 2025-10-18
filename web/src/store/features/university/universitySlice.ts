import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface UniversityStats {
  totalStudents: number;
  totalFaculty: number;
  totalStaff: number;
  totalPrograms: number;
  credentialsIssued: number;
  complianceScore: number;
}

export interface UniversityState {
  name: string;
  location: {
    city: string;
    state: string;
    country: string;
  };
  stats: UniversityStats;
  departments: string[];
  programs: string[];
  governanceFrameworks: string[];
  isLoading: boolean;
  error: string | null;
}

const initialState: UniversityState = {
  name: 'CollegiumAI Digital University',
  location: {
    city: 'Vienna',
    state: 'Vienna',
    country: 'Austria',
  },
  stats: {
    totalStudents: 0,
    totalFaculty: 0,
    totalStaff: 0,
    totalPrograms: 0,
    credentialsIssued: 0,
    complianceScore: 0,
  },
  departments: [],
  programs: [],
  governanceFrameworks: [],
  isLoading: false,
  error: null,
};

const universitySlice = createSlice({
  name: 'university',
  initialState,
  reducers: {
    setUniversityInfo: (state, action: PayloadAction<{ name: string; location: { city: string; state: string; country: string } }>) => {
      state.name = action.payload.name;
      state.location = action.payload.location;
    },
    setStats: (state, action: PayloadAction<UniversityStats>) => {
      state.stats = action.payload;
    },
    setDepartments: (state, action: PayloadAction<string[]>) => {
      state.departments = action.payload;
    },
    setPrograms: (state, action: PayloadAction<string[]>) => {
      state.programs = action.payload;
    },
    setGovernanceFrameworks: (state, action: PayloadAction<string[]>) => {
      state.governanceFrameworks = action.payload;
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
  setUniversityInfo,
  setStats,
  setDepartments,
  setPrograms,
  setGovernanceFrameworks,
  setLoading,
  setError,
} = universitySlice.actions;

export default universitySlice.reducer;