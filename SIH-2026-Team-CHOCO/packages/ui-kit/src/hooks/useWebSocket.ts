import { useEffect, useRef } from 'react';
import { io, Socket } from 'socket.io-client';
import { useDispatch } from 'react-redux';
import { addAlert } from '../store/slices/alertsSlice';

export const useWebSocket = () => {
  const socket = useRef<Socket | null>(null);
  const dispatch = useDispatch();

  useEffect(() => {
    const token = localStorage.getItem('access');
    const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';

    socket.current = io(wsUrl, {
      auth: { token },
      reconnectionDelay: 1000,
      reconnectionDelayMax: 8000,
    });

    // Automatically dispatch high-risk ML predictions to the Redux store
    socket.current.on('NEW_ALERT', (data) => {
      dispatch(addAlert({
        alert_id: crypto.randomUUID(),
        timestamp: new Date().toISOString(),
        ...data
      }));
    });

    return () => {
      socket.current?.disconnect();
    };
  }, [dispatch]);

  return socket.current;
};
