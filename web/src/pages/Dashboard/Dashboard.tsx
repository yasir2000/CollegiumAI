import React, { useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  LinearProgress,
  Chip,
  Avatar,
  IconButton,
  Paper
} from '@mui/material';
import {
  School as SchoolIcon,
  Psychology as PsychologyIcon,
  Groups as GroupsIcon,
  Analytics as AnalyticsIcon,
  Memory as MemoryIcon,
  TrendingUp as TrendingUpIcon,
  Speed as SpeedIcon,
  Security as SecurityIcon,
  PlayArrow as PlayArrowIcon,
  Refresh as RefreshIcon
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store/store';
import { addAlert } from '../../store/slices/systemSlice';

interface QuickStat {
  title: string;
  value: string | number;
  change?: string;
  color: 'primary' | 'secondary' | 'success' | 'warning' | 'error';
  icon: React.ReactNode;
}

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { currentPersona, availablePersonas } = useSelector((state: RootState) => state.persona);
  const { agents, collaborationMetrics } = useSelector((state: RootState) => state.agent);
  const { processes, insights } = useSelector((state: RootState) => state.cognitive);
  const { isOnline, health } = useSelector((state: RootState) => state.system);

  useEffect(() => {
    // Welcome message
    dispatch(addAlert({
      id: `welcome-${Date.now()}`,
      type: 'success',
      title: 'Welcome to CollegiumAI',
      message: 'Your intelligent university assistant is ready!',
      timestamp: new Date(),
    }));
  }, [dispatch]);

  const quickStats: QuickStat[] = [
    {
      title: 'Active Personas',
      value: availablePersonas.length || 51,
      change: '+12 this week',
      color: 'primary',
      icon: <SchoolIcon />
    },
    {
      title: 'Active Agents',
      value: agents.filter(a => a.status === 'active').length || 8,
      change: '100% uptime',
      color: 'success',
      icon: <GroupsIcon />
    },
    {
      title: 'Cognitive Processes',
      value: processes.filter(p => p.status === 'active').length || 7,
      change: '95% efficiency',
      color: 'secondary',
      icon: <MemoryIcon />
    },
    {
      title: 'Success Rate',
      value: `${collaborationMetrics.successRate || 94}%`,
      change: '+2.3% today',
      color: 'warning',
      icon: <TrendingUpIcon />
    }
  ];

  const recentInsights = insights.slice(0, 3);
  const activeProcesses = processes.filter(p => p.status === 'active').slice(0, 4);

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom fontWeight="bold">
          CollegiumAI Dashboard
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ mb: 2 }}>
          Next-Generation Intelligent University Assistant
        </Typography>
        
        {currentPersona && (
          <Card sx={{ mb: 3, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Avatar sx={{ bgcolor: 'rgba(255,255,255,0.2)', width: 60, height: 60 }}>
                  {currentPersona.name.charAt(0)}
                </Avatar>
                <Box sx={{ flexGrow: 1 }}>
                  <Typography variant="h5" gutterBottom>
                    Active Persona: {currentPersona.name}
                  </Typography>
                  <Typography variant="body1" sx={{ opacity: 0.9 }}>
                    {currentPersona.description}
                  </Typography>
                  <Chip 
                    label={currentPersona.type} 
                    sx={{ mt: 1, bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
                  />
                </Box>
                <Button 
                  variant="contained" 
                  onClick={() => navigate('/personas')}
                  sx={{ bgcolor: 'rgba(255,255,255,0.2)', '&:hover': { bgcolor: 'rgba(255,255,255,0.3)' } }}
                >
                  Switch Persona
                </Button>
              </Box>
            </CardContent>
          </Card>
        )}
      </Box>

      {/* Quick Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {quickStats.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box>
                    <Typography variant="h4" component="div" color={`${stat.color}.main`} fontWeight="bold">
                      {stat.value}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      {stat.title}
                    </Typography>
                    {stat.change && (
                      <Typography variant="caption" color="success.main">
                        {stat.change}
                      </Typography>
                    )}
                  </Box>
                  <Box sx={{ color: `${stat.color}.main` }}>
                    {stat.icon}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        {/* Quick Actions */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<PlayArrowIcon />}
                    onClick={() => navigate('/chat')}
                    sx={{ height: 60 }}
                  >
                    Start Chat
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<GroupsIcon />}
                    onClick={() => navigate('/multi-agent')}
                    sx={{ height: 60 }}
                  >
                    Multi-Agent
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<PsychologyIcon />}
                    onClick={() => navigate('/cognitive')}
                    sx={{ height: 60 }}
                  >
                    Cognitive Monitor
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    fullWidth
                    variant="outlined"
                    startIcon={<AnalyticsIcon />}
                    onClick={() => navigate('/analytics')}
                    sx={{ height: 60 }}
                  >
                    Analytics
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* System Health */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                <Typography variant="h6">
                  System Health
                </Typography>
                <IconButton size="small">
                  <RefreshIcon />
                </IconButton>
              </Box>
              
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">Overall Status</Typography>
                  <Chip 
                    label={health.toUpperCase()} 
                    color={health === 'excellent' ? 'success' : health === 'good' ? 'primary' : 'warning'}
                    size="small"
                  />
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={health === 'excellent' ? 100 : health === 'good' ? 80 : 60} 
                  color={health === 'excellent' ? 'success' : 'primary'}
                />
              </Box>

              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                <SpeedIcon color="primary" />
                <Typography variant="body2">Performance: Optimal</Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                <SecurityIcon color="success" />
                <Typography variant="body2">Security: All checks passed</Typography>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <MemoryIcon color="info" />
                <Typography variant="body2">Memory: {(Math.random() * 30 + 40).toFixed(1)}% used</Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Insights */}
        {recentInsights.length > 0 && (
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Recent Cognitive Insights
                </Typography>
                {recentInsights.map((insight) => (
                  <Paper 
                    key={insight.id} 
                    elevation={0} 
                    sx={{ p: 2, mb: 1, bgcolor: 'grey.50', border: 1, borderColor: 'grey.200' }}
                  >
                    <Typography variant="subtitle2" gutterBottom>
                      {insight.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {insight.description}
                    </Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
                      <Chip label={insight.type} size="small" />
                      <Typography variant="caption" color="text.secondary">
                        {insight.confidence}% confidence
                      </Typography>
                    </Box>
                  </Paper>
                ))}
                <Button variant="text" onClick={() => navigate('/cognitive')} fullWidth>
                  View All Insights
                </Button>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Active Processes */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Active Cognitive Processes
              </Typography>
              {activeProcesses.length > 0 ? activeProcesses.map((process) => (
                <Box key={process.id} sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                    <Typography variant="body2" fontWeight="medium">
                      {process.name}
                    </Typography>
                    <Chip 
                      label={process.type} 
                      size="small" 
                      color={process.status === 'active' ? 'success' : 'default'}
                    />
                  </Box>
                  <LinearProgress 
                    variant="determinate" 
                    value={process.efficiency} 
                    sx={{ mb: 1 }}
                  />
                  <Typography variant="caption" color="text.secondary">
                    Efficiency: {process.efficiency.toFixed(1)}%
                  </Typography>
                </Box>
              )) : (
                <Typography color="text.secondary">
                  No active processes - System in idle mode
                </Typography>
              )}
              <Button variant="text" onClick={() => navigate('/cognitive')} fullWidth>
                View Cognitive Monitor
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;