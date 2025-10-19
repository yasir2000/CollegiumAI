import React, { useState } from 'react';
import {
  Container,
  Typography,
  Card,
  CardContent,
  Box,
  Grid,
  Button,
  Chip,
  LinearProgress,
  Avatar,
  Tab,
  Tabs,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  ListItemSecondaryAction,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  Tooltip,
  Switch,
  FormControlLabel,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  SpeedDial,
  SpeedDialIcon,
  SpeedDialAction
} from '@mui/material';
import {
  Groups as GroupsIcon,
  Assignment as AssignmentIcon,
  TrendingUp as TrendingUpIcon,
  Add as AddIcon,
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Stop as StopIcon,
  Settings as SettingsIcon,
  Refresh as RefreshIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  Message as MessageIcon,
  Timeline as TimelineIcon,
  Assessment as AssessmentIcon,
  Psychology as PsychologyIcon,
  Engineering as EngineeringIcon,
  School as SchoolIcon,
  Security as SecurityIcon,
  Visibility as VisibilityIcon,
  Share as ShareIcon,
  Hub as HubIcon
} from '@mui/icons-material';

import WorkflowDesigner from '../../components/WorkflowDesigner/WorkflowDesigner';
import CommunicationHub from '../../components/CommunicationHub/CommunicationHub';
import AnalyticsDashboard from '../../components/AnalyticsDashboard/AnalyticsDashboard';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`agent-tabpanel-${index}`}
      aria-labelledby={`agent-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

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

interface Task {
  id: string;
  title: string;
  description: string;
  status: 'pending' | 'in-progress' | 'completed' | 'failed';
  priority: 'low' | 'medium' | 'high' | 'critical';
  assignedAgents: string[];
  createdAt: string;
  estimatedCompletion: string;
  progress: number;
  category: string;
}

interface Communication {
  id: string;
  fromAgent: string;
  toAgent: string;
  message: string;
  timestamp: string;
  type: 'info' | 'request' | 'response' | 'alert';
}

const MultiAgentWorkspace: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [openAgentDialog, setOpenAgentDialog] = useState(false);
  const [openTaskDialog, setOpenTaskDialog] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);
  const [newAgentType, setNewAgentType] = useState('');
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [realTimeEnabled, setRealTimeEnabled] = useState(true);

  // Mock data for agents
  const [agents, setAgents] = useState<Agent[]>([
    {
      id: 'agent-001',
      name: 'Alpha Research Agent',
      type: 'Research',
      status: 'active',
      specialization: 'Academic Research & Analysis',
      currentTask: 'Literature Review: AI Ethics',
      performance: 92,
      uptime: '72h 15m',
      tasksCompleted: 147,
      collaborations: 23,
      avatar: 'AR',
      capabilities: ['Research', 'Analysis', 'Writing', 'Citation'],
      memory: 85,
      processing: 78
    },
    {
      id: 'agent-002',
      name: 'Beta Engineering Agent',
      type: 'Engineering',
      status: 'busy',
      specialization: 'Software Development & Architecture',
      currentTask: 'Code Review: Multi-Agent Framework',
      performance: 88,
      uptime: '156h 42m',
      tasksCompleted: 203,
      collaborations: 31,
      avatar: 'BE',
      capabilities: ['Coding', 'Architecture', 'Testing', 'Optimization'],
      memory: 92,
      processing: 95
    },
    {
      id: 'agent-003',
      name: 'Gamma Analytics Agent',
      type: 'Analytics',
      status: 'idle',
      specialization: 'Data Analysis & Visualization',
      performance: 94,
      uptime: '98h 33m',
      tasksCompleted: 89,
      collaborations: 18,
      avatar: 'GA',
      capabilities: ['Data Analysis', 'Visualization', 'Statistics', 'ML'],
      memory: 76,
      processing: 82
    },
    {
      id: 'agent-004',
      name: 'Delta Communication Agent',
      type: 'Communication',
      status: 'active',
      specialization: 'Inter-Agent Coordination',
      currentTask: 'Facilitating Research-Engineering Collaboration',
      performance: 96,
      uptime: '124h 18m',
      tasksCompleted: 312,
      collaborations: 45,
      avatar: 'DC',
      capabilities: ['Coordination', 'Translation', 'Protocol', 'Routing'],
      memory: 68,
      processing: 73
    },
    {
      id: 'agent-005',
      name: 'Epsilon Security Agent',
      type: 'Security',
      status: 'active',
      specialization: 'System Security & Compliance',
      currentTask: 'Security Audit: Agent Communications',
      performance: 91,
      uptime: '187h 55m',
      tasksCompleted: 156,
      collaborations: 12,
      avatar: 'ES',
      capabilities: ['Security', 'Audit', 'Compliance', 'Monitoring'],
      memory: 89,
      processing: 87
    }
  ]);

  // Mock tasks data
  const [tasks, setTasks] = useState<Task[]>([
    {
      id: 'task-001',
      title: 'Multi-Agent Framework Enhancement',
      description: 'Enhance the multi-agent collaboration framework with new communication protocols',
      status: 'in-progress',
      priority: 'high',
      assignedAgents: ['agent-001', 'agent-002', 'agent-004'],
      createdAt: '2025-10-19T08:00:00Z',
      estimatedCompletion: '2025-10-20T16:00:00Z',
      progress: 67,
      category: 'Development'
    },
    {
      id: 'task-002',
      title: 'Performance Analytics Dashboard',
      description: 'Create comprehensive analytics dashboard for agent performance monitoring',
      status: 'in-progress',
      priority: 'medium',
      assignedAgents: ['agent-003', 'agent-002'],
      createdAt: '2025-10-19T10:30:00Z',
      estimatedCompletion: '2025-10-21T12:00:00Z',
      progress: 34,
      category: 'Analytics'
    },
    {
      id: 'task-003',
      title: 'Security Protocol Implementation',
      description: 'Implement enhanced security protocols for agent communications',
      status: 'pending',
      priority: 'critical',
      assignedAgents: ['agent-005', 'agent-004'],
      createdAt: '2025-10-19T14:15:00Z',
      estimatedCompletion: '2025-10-22T09:00:00Z',
      progress: 12,
      category: 'Security'
    }
  ]);

  // Mock communications data
  const [communications, setCommunications] = useState<Communication[]>([
    {
      id: 'comm-001',
      fromAgent: 'agent-001',
      toAgent: 'agent-002',
      message: 'Research findings ready for implementation review',
      timestamp: '2025-10-19T15:30:00Z',
      type: 'info'
    },
    {
      id: 'comm-002',
      fromAgent: 'agent-004',
      toAgent: 'agent-001',
      message: 'Task coordination updated - priority changed to high',
      timestamp: '2025-10-19T15:25:00Z',
      type: 'alert'
    },
    {
      id: 'comm-003',
      fromAgent: 'agent-002',
      toAgent: 'agent-003',
      message: 'Requesting data analysis for performance metrics',
      timestamp: '2025-10-19T15:20:00Z',
      type: 'request'
    }
  ]);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
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

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'info';
      case 'low': return 'success';
      default: return 'default';
    }
  };

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

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h3" component="h1" gutterBottom fontWeight="bold">
            Multi-Agent Collaboration Platform
          </Typography>
          <Typography variant="h6" color="text.secondary">
            Advanced AI agent coordination, monitoring, and collaboration system
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <FormControlLabel
            control={
              <Switch
                checked={realTimeEnabled}
                onChange={(e) => setRealTimeEnabled(e.target.checked)}
                color="primary"
              />
            }
            label="Real-time Updates"
          />
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setOpenAgentDialog(true)}
          >
            New Agent
          </Button>
          <Button
            variant="outlined"
            startIcon={<AssignmentIcon />}
            onClick={() => setOpenTaskDialog(true)}
          >
            New Task
          </Button>
        </Box>
      </Box>

      {/* Real-time Status Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)' }}>
            <CardContent sx={{ color: 'white', textAlign: 'center' }}>
              <GroupsIcon sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" fontWeight="bold">
                {agents.filter(a => a.status === 'active' || a.status === 'busy').length}
              </Typography>
              <Typography variant="body2">Active Agents</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #4CAF50 30%, #81C784 90%)' }}>
            <CardContent sx={{ color: 'white', textAlign: 'center' }}>
              <AssignmentIcon sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" fontWeight="bold">
                {tasks.filter(t => t.status === 'in-progress').length}
              </Typography>
              <Typography variant="body2">Active Tasks</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #FF9800 30%, #FFB74D 90%)' }}>
            <CardContent sx={{ color: 'white', textAlign: 'center' }}>
              <HubIcon sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" fontWeight="bold">
                {communications.length}
              </Typography>
              <Typography variant="body2">Communications</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #9C27B0 30%, #BA68C8 90%)' }}>
            <CardContent sx={{ color: 'white', textAlign: 'center' }}>
              <TrendingUpIcon sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" fontWeight="bold">
                {Math.round(agents.reduce((acc, agent) => acc + agent.performance, 0) / agents.length)}%
              </Typography>
              <Typography variant="body2">Avg Performance</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Main Content Tabs */}
      <Paper sx={{ width: '100%' }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
        >
          <Tab icon={<GroupsIcon />} label="Agent Network" />
          <Tab icon={<AssignmentIcon />} label="Task Management" />
          <Tab icon={<MessageIcon />} label="Communications" />
          <Tab icon={<AssessmentIcon />} label="Analytics" />
          <Tab icon={<TimelineIcon />} label="Workflows" />
          <Tab icon={<SettingsIcon />} label="Configuration" />
        </Tabs>

        {/* Agent Network Tab */}
        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={3}>
            {agents.map((agent) => (
              <Grid item xs={12} md={6} lg={4} key={agent.id}>
                <Card sx={{ height: '100%' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Avatar sx={{ mr: 2, bgcolor: 'primary.main' }}>
                        {getAgentIcon(agent.type)}
                      </Avatar>
                      <Box sx={{ flexGrow: 1 }}>
                        <Typography variant="h6">{agent.name}</Typography>
                        <Chip 
                          label={agent.status} 
                          size="small" 
                          color={getStatusColor(agent.status) as any}
                          sx={{ mr: 1 }}
                        />
                        <Chip label={agent.type} size="small" variant="outlined" />
                      </Box>
                      <IconButton onClick={() => setSelectedAgent(agent)}>
                        <SettingsIcon />
                      </IconButton>
                    </Box>
                    
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      {agent.specialization}
                    </Typography>
                    
                    {agent.currentTask && (
                      <Alert severity="info" sx={{ mb: 2, py: 0 }}>
                        <Typography variant="caption">
                          Current: {agent.currentTask}
                        </Typography>
                      </Alert>
                    )}
                    
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" gutterBottom>
                        Performance: {agent.performance}%
                      </Typography>
                      <LinearProgress 
                        variant="determinate" 
                        value={agent.performance} 
                        sx={{ mb: 1, height: 6, borderRadius: 3 }}
                      />
                    </Box>
                    
                    <Grid container spacing={1} sx={{ mb: 2 }}>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          Uptime: {agent.uptime}
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="caption" color="text.secondary">
                          Tasks: {agent.tasksCompleted}
                        </Typography>
                      </Grid>
                    </Grid>
                    
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <Tooltip title="Start Agent">
                        <IconButton size="small" color="success">
                          <PlayIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Pause Agent">
                        <IconButton size="small" color="warning">
                          <PauseIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="Stop Agent">
                        <IconButton size="small" color="error">
                          <StopIcon />
                        </IconButton>
                      </Tooltip>
                      <Tooltip title="View Details">
                        <IconButton size="small" color="primary">
                          <VisibilityIcon />
                        </IconButton>
                      </Tooltip>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>

        {/* Task Management Tab */}
        <TabPanel value={tabValue} index={1}>
          <Box sx={{ mb: 3 }}>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => setOpenTaskDialog(true)}
              sx={{ mr: 2 }}
            >
              Create Task
            </Button>
            <Button variant="outlined" startIcon={<RefreshIcon />}>
              Refresh Tasks
            </Button>
          </Box>
          
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Task</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Priority</TableCell>
                  <TableCell>Assigned Agents</TableCell>
                  <TableCell>Progress</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {tasks.map((task) => (
                  <TableRow key={task.id} hover>
                    <TableCell>
                      <Typography variant="subtitle2">{task.title}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        {task.description}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={task.status} 
                        size="small" 
                        color={task.status === 'completed' ? 'success' : 
                               task.status === 'in-progress' ? 'primary' : 'default'}
                      />
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={task.priority} 
                        size="small" 
                        color={getPriorityColor(task.priority) as any}
                      />
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 0.5 }}>
                        {task.assignedAgents.slice(0, 3).map((agentId) => {
                          const agent = agents.find(a => a.id === agentId);
                          return agent ? (
                            <Tooltip key={agentId} title={agent.name}>
                              <Avatar sx={{ width: 24, height: 24, fontSize: '0.7rem' }}>
                                {agent.avatar}
                              </Avatar>
                            </Tooltip>
                          ) : null;
                        })}
                        {task.assignedAgents.length > 3 && (
                          <Tooltip title={`+${task.assignedAgents.length - 3} more`}>
                            <Avatar sx={{ width: 24, height: 24, fontSize: '0.7rem' }}>
                              +{task.assignedAgents.length - 3}
                            </Avatar>
                          </Tooltip>
                        )}
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', width: '100px' }}>
                        <LinearProgress
                          variant="determinate"
                          value={task.progress}
                          sx={{ flexGrow: 1, mr: 1, height: 6, borderRadius: 3 }}
                        />
                        <Typography variant="caption">{task.progress}%</Typography>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Box sx={{ display: 'flex', gap: 0.5 }}>
                        <IconButton size="small" color="primary">
                          <EditIcon />
                        </IconButton>
                        <IconButton size="small" color="success">
                          <PlayIcon />
                        </IconButton>
                        <IconButton size="small" color="error">
                          <DeleteIcon />
                        </IconButton>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </TabPanel>

        {/* Communications Tab */}
        <TabPanel value={tabValue} index={2}>
          <CommunicationHub />
        </TabPanel>

        {/* Analytics Tab */}
        <TabPanel value={tabValue} index={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Agent Performance Metrics
                  </Typography>
                  {agents.map((agent) => (
                    <Box key={agent.id} sx={{ mb: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="body2">{agent.name}</Typography>
                        <Typography variant="body2">{agent.performance}%</Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={agent.performance}
                        sx={{ height: 8, borderRadius: 4 }}
                      />
                    </Box>
                  ))}
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    System Resources
                  </Typography>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" gutterBottom>
                      Memory Usage: {Math.round(agents.reduce((acc, agent) => acc + agent.memory, 0) / agents.length)}%
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={Math.round(agents.reduce((acc, agent) => acc + agent.memory, 0) / agents.length)}
                      sx={{ height: 8, borderRadius: 4, mb: 2 }}
                    />
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" gutterBottom>
                      Processing Power: {Math.round(agents.reduce((acc, agent) => acc + agent.processing, 0) / agents.length)}%
                    </Typography>
                    <LinearProgress
                      variant="determinate"
                      value={Math.round(agents.reduce((acc, agent) => acc + agent.processing, 0) / agents.length)}
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Workflows Tab */}
        <TabPanel value={tabValue} index={4}>
          <WorkflowDesigner />
        </TabPanel>

        {/* Configuration Tab */}
        <TabPanel value={tabValue} index={5}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    System Configuration
                  </Typography>
                  <FormControlLabel
                    control={<Switch defaultChecked />}
                    label="Auto-scaling Enabled"
                  />
                  <FormControlLabel
                    control={<Switch defaultChecked />}
                    label="Load Balancing"
                  />
                  <FormControlLabel
                    control={<Switch />}
                    label="Debug Mode"
                  />
                  <FormControlLabel
                    control={<Switch defaultChecked />}
                    label="Performance Monitoring"
                  />
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Communication Protocols
                  </Typography>
                  <TextField
                    fullWidth
                    label="Max Message Size (KB)"
                    defaultValue="1024"
                    type="number"
                    sx={{ mb: 2 }}
                  />
                  <TextField
                    fullWidth
                    label="Timeout (seconds)"
                    defaultValue="30"
                    type="number"
                    sx={{ mb: 2 }}
                  />
                  <FormControl fullWidth>
                    <InputLabel>Protocol Version</InputLabel>
                    <Select defaultValue="v2.1" label="Protocol Version">
                      <MenuItem value="v2.0">v2.0 (Stable)</MenuItem>
                      <MenuItem value="v2.1">v2.1 (Current)</MenuItem>
                      <MenuItem value="v2.2">v2.2 (Beta)</MenuItem>
                    </Select>
                  </FormControl>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>
      </Paper>

      {/* Floating Action Button for Quick Actions */}
      <SpeedDial
        ariaLabel="Quick Actions"
        sx={{ position: 'fixed', bottom: 16, right: 16 }}
        icon={<SpeedDialIcon />}
      >
        <SpeedDialAction
          key="new-agent"
          icon={<AddIcon />}
          tooltipTitle="New Agent"
          onClick={() => setOpenAgentDialog(true)}
        />
        <SpeedDialAction
          key="new-task"
          icon={<AssignmentIcon />}
          tooltipTitle="New Task"
          onClick={() => setOpenTaskDialog(true)}
        />
        <SpeedDialAction
          key="refresh"
          icon={<RefreshIcon />}
          tooltipTitle="Refresh"
        />
      </SpeedDial>

      {/* New Agent Dialog */}
      <Dialog open={openAgentDialog} onClose={() => setOpenAgentDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Create New Agent</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              fullWidth
              label="Agent Name"
              placeholder="Enter agent name"
              sx={{ mb: 2 }}
            />
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Agent Type</InputLabel>
              <Select
                value={newAgentType}
                label="Agent Type"
                onChange={(e) => setNewAgentType(e.target.value)}
              >
                <MenuItem value="Research">Research Agent</MenuItem>
                <MenuItem value="Engineering">Engineering Agent</MenuItem>
                <MenuItem value="Analytics">Analytics Agent</MenuItem>
                <MenuItem value="Communication">Communication Agent</MenuItem>
                <MenuItem value="Security">Security Agent</MenuItem>
                <MenuItem value="General">General Purpose Agent</MenuItem>
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="Specialization"
              placeholder="Enter agent specialization"
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Capabilities"
              placeholder="List agent capabilities (comma-separated)"
              multiline
              rows={3}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAgentDialog(false)}>Cancel</Button>
          <Button variant="contained" onClick={() => setOpenAgentDialog(false)}>
            Create Agent
          </Button>
        </DialogActions>
      </Dialog>

      {/* New Task Dialog */}
      <Dialog open={openTaskDialog} onClose={() => setOpenTaskDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Create New Task</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              fullWidth
              label="Task Title"
              placeholder="Enter task title"
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Description"
              placeholder="Enter task description"
              multiline
              rows={3}
              sx={{ mb: 2 }}
            />
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Priority</InputLabel>
              <Select defaultValue="medium" label="Priority">
                <MenuItem value="low">Low</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="high">High</MenuItem>
                <MenuItem value="critical">Critical</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>Category</InputLabel>
              <Select defaultValue="general" label="Category">
                <MenuItem value="development">Development</MenuItem>
                <MenuItem value="research">Research</MenuItem>
                <MenuItem value="analytics">Analytics</MenuItem>
                <MenuItem value="security">Security</MenuItem>
                <MenuItem value="general">General</MenuItem>
              </Select>
            </FormControl>
            <TextField
              fullWidth
              label="Estimated Completion"
              type="datetime-local"
              InputLabelProps={{ shrink: true }}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenTaskDialog(false)}>Cancel</Button>
          <Button variant="contained" onClick={() => setOpenTaskDialog(false)}>
            Create Task
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default MultiAgentWorkspace;