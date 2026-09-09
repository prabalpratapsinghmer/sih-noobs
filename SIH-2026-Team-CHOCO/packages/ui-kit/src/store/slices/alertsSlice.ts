import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

export interface AlertPayload {
  alert_id: string;
  complaint_ref: string;
  atm_id: string;
  risk_score: number;
  message: string;
  timestamp: string;
  isRead: boolean;
}

interface AlertsState {
  activeAlerts: AlertPayload[];
  unreadCount: number;
}

const initialState: AlertsState = {
  activeAlerts: [],
  unreadCount: 0,
};

export const alertsSlice = createSlice({
  name: 'alerts',
  initialState,
  reducers: {
    addAlert: (state, action: PayloadAction<Omit<AlertPayload, 'isRead'>>) => {
      state.activeAlerts.unshift({ ...action.payload, isRead: false });
      state.unreadCount += 1;
    },
    markAsRead: (state, action: PayloadAction<string>) => {
      const alert = state.activeAlerts.find(a => a.alert_id === action.payload);
      if (alert && !alert.isRead) {
        alert.isRead = true;
        state.unreadCount = Math.max(0, state.unreadCount - 1);
      }
    },
    clearAll: (state) => {
      state.activeAlerts = [];
      state.unreadCount = 0;
    }
  },
});

export const { addAlert, markAsRead, clearAll } = alertsSlice.actions;
export const alertsReducer = alertsSlice.reducer;
