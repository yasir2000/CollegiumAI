import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface SystemMetrics {
  cpu: number;
  memory: number;
  responseTime: number;
  throughput: number;
  activeConnections: number;
  timestamp: Date;
}

export interface SystemAlert {
  id: string;
  type: 'info' | 'warning' | 'error' | 'success';
  title: string;
  message: string;
  timestamp: Date;
  dismissed?: boolean;
}

interface SystemState {
  isOnline: boolean;
  health: 'excellent' | 'good' | 'fair' | 'poor' | 'critical';
  metrics: SystemMetrics | null;
  alerts: SystemAlert[];
  lastUpdateTime: Date | null;
  performanceHistory: SystemMetrics[];
  version: string;
  uptime: number;
  error: string | null;
}

const initialState: SystemState = {
  isOnline: false,
  health: 'good',
  metrics: null,
  alerts: [],
  lastUpdateTime: null,
  performanceHistory: [],
  version: '2.0.0',
  uptime: 0,
  error: null,
};

const systemSlice = createSlice({
  name: 'system',
  initialState,
  reducers: {
    setOnlineStatus: (state, action: PayloadAction<boolean>) => {
      state.isOnline = action.payload;
    },
    setHealth: (state, action: PayloadAction<SystemState['health']>) => {
      state.health = action.payload;
    },
    updateMetrics: (state, action: PayloadAction<SystemMetrics>) => {
      state.metrics = action.payload;
      state.performanceHistory.push(action.payload);
      // Keep only last 100 metrics for performance
      if (state.performanceHistory.length > 100) {
        state.performanceHistory = state.performanceHistory.slice(-100);
      }
      state.lastUpdateTime = new Date();
    },
    addAlert: (state, action: PayloadAction<SystemAlert>) => {
      state.alerts.unshift(action.payload);
      // Keep only last 50 alerts
      if (state.alerts.length > 50) {
        state.alerts = state.alerts.slice(0, 50);
      }
    },
    dismissAlert: (state, action: PayloadAction<string>) => {
      const alert = state.alerts.find(alert => alert.id === action.payload);
      if (alert) {
        alert.dismissed = true;
      }
    },
    clearDismissedAlerts: (state) => {
      state.alerts = state.alerts.filter(alert => !alert.dismissed);
    },
    updateUptime: (state, action: PayloadAction<number>) => {
      state.uptime = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const {
  setOnlineStatus,
  setHealth,
  updateMetrics,
  addAlert,
  dismissAlert,
  clearDismissedAlerts,
  updateUptime,
  setError,
} = systemSlice.actions;

export default systemSlice.reducer;