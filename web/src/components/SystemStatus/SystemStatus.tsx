import React, { useEffect } from 'react';
import { 
  Box, 
  Paper, 
  Typography, 
  LinearProgress, 
  Chip,
  Grid
} from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store/store';
import { 
  setOnlineStatus, 
  updateMetrics, 
  setHealth, 
  updateUptime,
  SystemMetrics 
} from '../../store/slices/systemSlice';

const SystemStatus: React.FC = () => {
  const dispatch = useDispatch();
  const { isOnline, health, metrics, uptime } = useSelector((state: RootState) => state.system);

  useEffect(() => {
    // Simulate system monitoring
    const interval = setInterval(() => {
      // Simulate metrics
      const mockMetrics: SystemMetrics = {
        cpu: Math.random() * 100,
        memory: Math.random() * 100,
        responseTime: Math.random() * 1000,
        throughput: Math.random() * 100,
        activeConnections: Math.floor(Math.random() * 50),
        timestamp: new Date(),
      };

      dispatch(updateMetrics(mockMetrics));
      dispatch(setOnlineStatus(true));
      dispatch(updateUptime(uptime + 1));

      // Update health based on metrics
      const avgLoad = (mockMetrics.cpu + mockMetrics.memory) / 2;
      if (avgLoad < 30) dispatch(setHealth('excellent'));
      else if (avgLoad < 50) dispatch(setHealth('good'));
      else if (avgLoad < 70) dispatch(setHealth('fair'));
      else if (avgLoad < 90) dispatch(setHealth('poor'));
      else dispatch(setHealth('critical'));
    }, 5000);

    return () => clearInterval(interval);
  }, [dispatch, uptime]);

  const getHealthColor = (health: string) => {
    switch (health) {
      case 'excellent': return 'success';
      case 'good': return 'primary';
      case 'fair': return 'warning';
      case 'poor': return 'error';
      case 'critical': return 'error';
      default: return 'default';
    }
  };

  if (!metrics) return null;

  return (
    <Paper 
      elevation={1} 
      sx={{ 
        position: 'fixed', 
        bottom: 0, 
        left: 0, 
        right: 0, 
        p: 1, 
        bgcolor: 'background.paper',
        borderTop: 1,
        borderColor: 'divider',
        zIndex: 1000
      }}
    >
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} md={2}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Chip
              label={`System ${health.toUpperCase()}`}
              color={getHealthColor(health) as any}
              size="small"
            />
            <Chip
              label={isOnline ? 'Online' : 'Offline'}
              color={isOnline ? 'success' : 'error'}
              size="small"
            />
          </Box>
        </Grid>
        
        <Grid item xs={12} md={2}>
          <Box>
            <Typography variant="caption" color="text.secondary">
              CPU: {metrics.cpu.toFixed(1)}%
            </Typography>
            <LinearProgress 
              variant="determinate" 
              value={metrics.cpu} 
              sx={{ height: 4, borderRadius: 2 }}
              color={metrics.cpu > 80 ? 'error' : 'primary'}
            />
          </Box>
        </Grid>

        <Grid item xs={12} md={2}>
          <Box>
            <Typography variant="caption" color="text.secondary">
              Memory: {metrics.memory.toFixed(1)}%
            </Typography>
            <LinearProgress 
              variant="determinate" 
              value={metrics.memory} 
              sx={{ height: 4, borderRadius: 2 }}
              color={metrics.memory > 80 ? 'error' : 'primary'}
            />
          </Box>
        </Grid>

        <Grid item xs={12} md={2}>
          <Typography variant="caption" color="text.secondary">
            Response: {metrics.responseTime.toFixed(0)}ms
          </Typography>
        </Grid>

        <Grid item xs={12} md={2}>
          <Typography variant="caption" color="text.secondary">
            Connections: {metrics.activeConnections}
          </Typography>
        </Grid>

        <Grid item xs={12} md={2}>
          <Typography variant="caption" color="text.secondary">
            Uptime: {Math.floor(uptime / 60)}m {uptime % 60}s
          </Typography>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default SystemStatus;