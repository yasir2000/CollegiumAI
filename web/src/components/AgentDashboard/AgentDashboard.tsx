import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Grid,
  Button,
  Chip,
  LinearProgress,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Divider,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Tooltip,
  Badge
} from '@mui/material';
import {
  Memory as MemoryIcon,
  Speed as SpeedIcon,
  Timeline as TimelineIcon,
  TrendingUp as TrendingUpIcon,
  Assignment as AssignmentIcon,
  Message as MessageIcon,
  Settings as SettingsIcon,
  Close as CloseIcon,
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Stop as StopIcon,
  Refresh as RefreshIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Psychology as PsychologyIcon,
  Engineering as EngineeringIcon,
  School as SchoolIcon,
  Security as SecurityIcon,
  Assessment as AssessmentIcon
} from '@mui/icons-material';

interface Agent {
  id: string;
  name: string;
  type: string;
  status: 'active' | 'idle' | 'busy' | 'error' | 'offline';
  specialization: string;
  currentTask?: string;
  performance: number;
  uptime: string;
  tasksCompleted: number;
  collaborations: number;
  avatar: string;
  capabilities: string[];
  memory: number;
  processing: number;
}

interface AgentDashboardProps {
  agent: Agent;
}

const AgentDashboard: React.FC<AgentDashboardProps> = ({ agent }) => {
  const [configOpen, setConfigOpen] = useState(false);

  const getAgentIcon = (type: string) => {
    switch (type) {
      case 'Research': return <SchoolIcon />;
      case 'Engineering': return <EngineeringIcon />;
      case 'Analytics': return <AssessmentIcon />;
      case 'Communication': return <MessageIcon />;
      case 'Security': return <SecurityIcon />;
      default: return <PsychologyIcon />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success';
      case 'busy': return 'warning';
      case 'idle': return 'info';
      case 'error': return 'error';
      case 'offline': return 'default';
      default: return 'default';
    }
  };

  const recentTasks = [
    { id: 1, title: 'Data Analysis Report', status: 'completed', time: '2 hours ago' },
    { id: 2, title: 'Algorithm Optimization', status: 'in-progress', time: '30 minutes ago' },
    { id: 3, title: 'Code Review', status: 'pending', time: '1 hour ago' }
  ];

  const performanceMetrics = [
    { label: 'Task Success Rate', value: 94, color: 'success' },
    { label: 'Response Time', value: 87, color: 'primary' },
    { label: 'Resource Efficiency', value: 89, color: 'info' },
    { label: 'Collaboration Score', value: 92, color: 'secondary' }
  ];

  return (
    <Box>
      {/* Agent Header */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Avatar sx={{ width: 64, height: 64, mr: 2, bgcolor: 'primary.main' }}>
              {getAgentIcon(agent.type)}
            </Avatar>
            <Box sx={{ flexGrow: 1 }}>
              <Typography variant="h4" fontWeight="bold">
                {agent.name}
              </Typography>
              <Typography variant="subtitle1" color="text.secondary">
                {agent.specialization}
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                <Chip 
                  label={agent.status} 
                  color={getStatusColor(agent.status) as any}
                  size="small" 
                />
                <Chip label={agent.type} variant="outlined" size="small" />
              </Box>
            </Box>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Tooltip title="Start Agent">
                <IconButton color="success">
                  <PlayIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title="Pause Agent">
                <IconButton color="warning">
                  <PauseIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title="Stop Agent">
                <IconButton color="error">
                  <StopIcon />
                </IconButton>
              </Tooltip>
              <Tooltip title="Configure">
                <IconButton onClick={() => setConfigOpen(true)}>
                  <SettingsIcon />
                </IconButton>
              </Tooltip>
            </Box>
          </Box>

          {agent.currentTask && (
            <Alert severity="info" sx={{ mb: 2 }}>
              <Typography variant="body2">
                <strong>Current Task:</strong> {agent.currentTask}
              </Typography>
            </Alert>
          )}
        </CardContent>
      </Card>

      <Grid container spacing={3}>
        {/* Performance Overview */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <TrendingUpIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Performance Overview
              </Typography>
              <Box sx={{ mb: 3 }}>
                <Typography variant="h3" color="primary" fontWeight="bold">
                  {agent.performance}%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Overall Performance Score
                </Typography>
              </Box>
              
              {performanceMetrics.map((metric, index) => (
                <Box key={index} sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                    <Typography variant="body2">{metric.label}</Typography>
                    <Typography variant="body2">{metric.value}%</Typography>
                  </Box>
                  <LinearProgress
                    variant="determinate"
                    value={metric.value}
                    color={metric.color as any}
                    sx={{ height: 6, borderRadius: 3 }}
                  />
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>

        {/* Resource Usage */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <MemoryIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Resource Usage
              </Typography>
              
              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" gutterBottom>
                  Memory Usage: {agent.memory}%
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={agent.memory}
                  sx={{ height: 8, borderRadius: 4, mb: 2 }}
                />
              </Box>

              <Box sx={{ mb: 3 }}>
                <Typography variant="body2" gutterBottom>
                  Processing Power: {agent.processing}%
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={agent.processing}
                  color="secondary"
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>

              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Uptime: {agent.uptime}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Tasks: {agent.tasksCompleted}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Tasks */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <AssignmentIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Recent Tasks
              </Typography>
              <List>
                {recentTasks.map((task) => (
                  <ListItem key={task.id} divider>
                    <ListItemIcon>
                      <AssignmentIcon color="primary" />
                    </ListItemIcon>
                    <ListItemText
                      primary={task.title}
                      secondary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Chip 
                            label={task.status} 
                            size="small" 
                            color={task.status === 'completed' ? 'success' : 
                                   task.status === 'in-progress' ? 'primary' : 'default'}
                          />
                          <Typography variant="caption">{task.time}</Typography>
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Capabilities */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <PsychologyIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Agent Capabilities
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {agent.capabilities.map((capability, index) => (
                  <Chip 
                    key={index} 
                    label={capability} 
                    variant="outlined" 
                    size="small"
                  />
                ))}
              </Box>
              <Divider sx={{ my: 2 }} />
              <Typography variant="body2" color="text.secondary">
                Collaborations: {agent.collaborations} active partnerships
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Activity Timeline */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <TimelineIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Activity Timeline
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Time</TableCell>
                      <TableCell>Activity</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Duration</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    <TableRow>
                      <TableCell>15:30</TableCell>
                      <TableCell>Started task: Algorithm Optimization</TableCell>
                      <TableCell>
                        <Chip label="In Progress" color="primary" size="small" />
                      </TableCell>
                      <TableCell>30 min</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>14:45</TableCell>
                      <TableCell>Completed: Data Analysis Report</TableCell>
                      <TableCell>
                        <Chip label="Completed" color="success" size="small" />
                      </TableCell>
                      <TableCell>2h 15min</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell>12:30</TableCell>
                      <TableCell>Collaboration initiated with Beta Engineering</TableCell>
                      <TableCell>
                        <Chip label="Active" color="info" size="small" />
                      </TableCell>
                      <TableCell>3h</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Configuration Dialog */}
      <Dialog open={configOpen} onClose={() => setConfigOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          Agent Configuration: {agent.name}
          <IconButton
            onClick={() => setConfigOpen(false)}
            sx={{ position: 'absolute', right: 8, top: 8 }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Agent Name"
                defaultValue={agent.name}
                sx={{ mb: 2 }}
              />
              <TextField
                fullWidth
                label="Specialization"
                defaultValue={agent.specialization}
                sx={{ mb: 2 }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Memory Limit (GB)"
                type="number"
                defaultValue="8"
                sx={{ mb: 2 }}
              />
              <TextField
                fullWidth
                label="CPU Allocation (%)"
                type="number"
                defaultValue="75"
                sx={{ mb: 2 }}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Capabilities"
                defaultValue={agent.capabilities.join(', ')}
                multiline
                rows={3}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setConfigOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={() => setConfigOpen(false)}>
            Save Configuration
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AgentDashboard;