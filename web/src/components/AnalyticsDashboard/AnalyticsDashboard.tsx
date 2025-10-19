import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  Chip,
  Avatar,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  LinearProgress,
  CircularProgress,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Switch,
  FormControlLabel,
  Tooltip,
  Alert
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  Analytics as AnalyticsIcon,
  Speed as SpeedIcon,
  Memory as MemoryIcon,
  Storage as StorageIcon,
  NetworkCheck as NetworkIcon,
  Assessment as AssessmentIcon,
  Timeline as TimelineIcon,
  PieChart as PieChartIcon,
  BarChart as BarChartIcon,
  ShowChart as ShowChartIcon,
  Refresh as RefreshIcon,
  Download as DownloadIcon,
  Settings as SettingsIcon,
  Fullscreen as FullscreenIcon,
  Close as CloseIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon
} from '@mui/icons-material';

interface MetricData {
  id: string;
  name: string;
  value: number;
  unit: string;
  trend: 'up' | 'down' | 'stable';
  trendValue: number;
  status: 'good' | 'warning' | 'critical';
}

interface PerformanceData {
  agentId: string;
  agentName: string;
  cpuUsage: number;
  memoryUsage: number;
  tasksCompleted: number;
  successRate: number;
  avgResponseTime: number;
  status: 'active' | 'idle' | 'error';
}

interface SystemHealth {
  component: string;
  status: 'healthy' | 'warning' | 'critical';
  uptime: string;
  lastCheck: string;
  issues: string[];
}

const AnalyticsDashboard: React.FC = () => {
  const [timeRange, setTimeRange] = useState('24h');
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [selectedMetric, setSelectedMetric] = useState<string | null>(null);
  const [fullscreenDialog, setFullscreenDialog] = useState(false);

  const systemMetrics: MetricData[] = [
    {
      id: 'total-agents',
      name: 'Total Agents',
      value: 12,
      unit: '',
      trend: 'up',
      trendValue: 2,
      status: 'good'
    },
    {
      id: 'active-tasks',
      name: 'Active Tasks',
      value: 847,
      unit: '',
      trend: 'up',
      trendValue: 12,
      status: 'good'
    },
    {
      id: 'avg-response-time',
      name: 'Avg Response Time',
      value: 0.34,
      unit: 's',
      trend: 'down',
      trendValue: 15,
      status: 'good'
    },
    {
      id: 'success-rate',
      name: 'Success Rate',
      value: 98.7,
      unit: '%',
      trend: 'up',
      trendValue: 1.2,
      status: 'good'
    },
    {
      id: 'cpu-usage',
      name: 'CPU Usage',
      value: 67,
      unit: '%',
      trend: 'up',
      trendValue: 8,
      status: 'warning'
    },
    {
      id: 'memory-usage',
      name: 'Memory Usage',
      value: 4.2,
      unit: 'GB',
      trend: 'stable',
      trendValue: 0,
      status: 'good'
    }
  ];

  const performanceData: PerformanceData[] = [
    {
      agentId: 'agent-001',
      agentName: 'Alpha Research Agent',
      cpuUsage: 45,
      memoryUsage: 512,
      tasksCompleted: 127,
      successRate: 99.2,
      avgResponseTime: 0.28,
      status: 'active'
    },
    {
      agentId: 'agent-002',
      agentName: 'Beta Engineering Agent',
      cpuUsage: 78,
      memoryUsage: 1024,
      tasksCompleted: 94,
      successRate: 97.8,
      avgResponseTime: 0.45,
      status: 'active'
    },
    {
      agentId: 'agent-003',
      agentName: 'Gamma Analytics Agent',
      cpuUsage: 23,
      memoryUsage: 256,
      tasksCompleted: 203,
      successRate: 99.8,
      avgResponseTime: 0.12,
      status: 'active'
    },
    {
      agentId: 'agent-004',
      agentName: 'Delta Communication Agent',
      cpuUsage: 56,
      memoryUsage: 384,
      tasksCompleted: 156,
      successRate: 98.5,
      avgResponseTime: 0.35,
      status: 'active'
    },
    {
      agentId: 'agent-005',
      agentName: 'Epsilon Security Agent',
      cpuUsage: 0,
      memoryUsage: 128,
      tasksCompleted: 0,
      successRate: 0,
      avgResponseTime: 0,
      status: 'idle'
    }
  ];

  const systemHealth: SystemHealth[] = [
    {
      component: 'Communication Hub',
      status: 'healthy',
      uptime: '99.9%',
      lastCheck: '2 min ago',
      issues: []
    },
    {
      component: 'Task Orchestrator',
      status: 'healthy',
      uptime: '99.7%',
      lastCheck: '1 min ago',
      issues: []
    },
    {
      component: 'Agent Manager',
      status: 'warning',
      uptime: '98.2%',
      lastCheck: '3 min ago',
      issues: ['High memory usage detected', 'Connection timeout warnings']
    },
    {
      component: 'Data Storage',
      status: 'healthy',
      uptime: '100%',
      lastCheck: '1 min ago',
      issues: []
    },
    {
      component: 'Security Layer',
      status: 'critical',
      uptime: '95.1%',
      lastCheck: '5 min ago',
      issues: ['Authentication service offline', 'SSL certificate expiring soon']
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'good':
      case 'healthy':
      case 'active':
        return 'success';
      case 'warning':
        return 'warning';
      case 'critical':
      case 'error':
        return 'error';
      case 'idle':
        return 'info';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'good':
      case 'healthy':
      case 'active':
        return <CheckCircleIcon color="success" />;
      case 'warning':
        return <WarningIcon color="warning" />;
      case 'critical':
      case 'error':
        return <ErrorIcon color="error" />;
      default:
        return <CheckCircleIcon color="disabled" />;
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'up':
        return <TrendingUpIcon color="success" fontSize="small" />;
      case 'down':
        return <TrendingDownIcon color="primary" fontSize="small" />;
      default:
        return null;
    }
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5" fontWeight="bold">
          <AnalyticsIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
          Multi-Agent Analytics
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel>Time Range</InputLabel>
            <Select
              value={timeRange}
              label="Time Range"
              onChange={(e) => setTimeRange(e.target.value)}
            >
              <MenuItem value="1h">Last Hour</MenuItem>
              <MenuItem value="24h">Last 24 Hours</MenuItem>
              <MenuItem value="7d">Last 7 Days</MenuItem>
              <MenuItem value="30d">Last 30 Days</MenuItem>
            </Select>
          </FormControl>
          <FormControlLabel
            control={
              <Switch
                checked={autoRefresh}
                onChange={(e) => setAutoRefresh(e.target.checked)}
                size="small"
              />
            }
            label="Auto Refresh"
          />
          <IconButton onClick={() => {}}>
            <RefreshIcon />
          </IconButton>
          <IconButton onClick={() => {}}>
            <DownloadIcon />
          </IconButton>
        </Box>
      </Box>

      {/* Key Metrics */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {systemMetrics.map((metric) => (
          <Grid item xs={12} sm={6} md={4} lg={2} key={metric.id}>
            <Card
              sx={{
                cursor: 'pointer',
                transition: 'all 0.2s',
                '&:hover': { transform: 'translateY(-2px)', boxShadow: 3 }
              }}
              onClick={() => setSelectedMetric(metric.id)}
            >
              <CardContent sx={{ textAlign: 'center', py: 2 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 1 }}>
                  <Typography variant="h4" fontWeight="bold" color="primary.main">
                    {metric.value}
                  </Typography>
                  <Typography variant="h6" color="text.secondary" sx={{ ml: 0.5 }}>
                    {metric.unit}
                  </Typography>
                </Box>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {metric.name}
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 0.5 }}>
                  {getTrendIcon(metric.trend)}
                  <Typography variant="caption" color="text.secondary">
                    {metric.trendValue > 0 && metric.trend !== 'stable' && (
                      <>
                        {metric.trend === 'up' ? '+' : '-'}{metric.trendValue}%
                      </>
                    )}
                    {metric.trend === 'stable' && 'Stable'}
                  </Typography>
                  <Chip
                    label={metric.status}
                    size="small"
                    color={getStatusColor(metric.status) as any}
                    sx={{ ml: 1 }}
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        {/* Performance Table */}
        <Grid item xs={12} lg={8}>
          <Card sx={{ height: '500px', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  <AssessmentIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Agent Performance Metrics
                </Typography>
                <IconButton size="small" onClick={() => setFullscreenDialog(true)}>
                  <FullscreenIcon />
                </IconButton>
              </Box>
              <TableContainer sx={{ flexGrow: 1 }}>
                <Table stickyHeader>
                  <TableHead>
                    <TableRow>
                      <TableCell>Agent</TableCell>
                      <TableCell align="center">Status</TableCell>
                      <TableCell align="center">CPU</TableCell>
                      <TableCell align="center">Memory</TableCell>
                      <TableCell align="center">Tasks</TableCell>
                      <TableCell align="center">Success Rate</TableCell>
                      <TableCell align="center">Avg Response</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {performanceData.map((agent) => (
                      <TableRow key={agent.agentId} hover>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
                              {agent.agentName.split(' ').map(n => n[0]).join('')}
                            </Avatar>
                            <Typography variant="body2">{agent.agentName}</Typography>
                          </Box>
                        </TableCell>
                        <TableCell align="center">
                          <Chip
                            label={agent.status}
                            size="small"
                            color={getStatusColor(agent.status) as any}
                          />
                        </TableCell>
                        <TableCell align="center">
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <LinearProgress
                              variant="determinate"
                              value={agent.cpuUsage}
                              sx={{ width: 60, height: 6 }}
                              color={agent.cpuUsage > 80 ? 'error' : agent.cpuUsage > 60 ? 'warning' : 'primary'}
                            />
                            <Typography variant="caption">{agent.cpuUsage}%</Typography>
                          </Box>
                        </TableCell>
                        <TableCell align="center">
                          <Typography variant="body2">{agent.memoryUsage} MB</Typography>
                        </TableCell>
                        <TableCell align="center">
                          <Typography variant="body2">{agent.tasksCompleted}</Typography>
                        </TableCell>
                        <TableCell align="center">
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <CircularProgress
                              variant="determinate"
                              value={agent.successRate}
                              size={24}
                              thickness={6}
                              color={agent.successRate > 95 ? 'success' : 'warning'}
                            />
                            <Typography variant="caption">{agent.successRate}%</Typography>
                          </Box>
                        </TableCell>
                        <TableCell align="center">
                          <Typography variant="body2">{agent.avgResponseTime}s</Typography>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* System Health */}
        <Grid item xs={12} lg={4}>
          <Card sx={{ height: '500px', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
              <Typography variant="h6" gutterBottom>
                <NetworkIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                System Health
              </Typography>
              <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
                {systemHealth.map((component, index) => (
                  <Paper key={index} sx={{ p: 2, mb: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="subtitle2">{component.component}</Typography>
                      {getStatusIcon(component.status)}
                    </Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="caption" color="text.secondary">
                        Uptime: {component.uptime}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {component.lastCheck}
                      </Typography>
                    </Box>
                    {component.issues.length > 0 && (
                      <Box>
                        {component.issues.map((issue, issueIndex) => (
                          <Alert key={issueIndex} severity="warning" sx={{ mt: 1, py: 0 }}>
                            <Typography variant="caption">{issue}</Typography>
                          </Alert>
                        ))}
                      </Box>
                    )}
                  </Paper>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Resource Utilization Charts */}
        <Grid item xs={12}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <SpeedIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                  <Typography variant="h6" gutterBottom>CPU Utilization</Typography>
                  <Typography variant="h4" color="primary.main">67%</Typography>
                  <LinearProgress
                    variant="determinate"
                    value={67}
                    sx={{ mt: 2, height: 8 }}
                    color="warning"
                  />
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <MemoryIcon sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                  <Typography variant="h6" gutterBottom>Memory Usage</Typography>
                  <Typography variant="h4" color="success.main">4.2 GB</Typography>
                  <LinearProgress
                    variant="determinate"
                    value={52}
                    sx={{ mt: 2, height: 8 }}
                    color="success"
                  />
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <StorageIcon sx={{ fontSize: 40, color: 'info.main', mb: 1 }} />
                  <Typography variant="h6" gutterBottom>Storage Used</Typography>
                  <Typography variant="h4" color="info.main">1.8 TB</Typography>
                  <LinearProgress
                    variant="determinate"
                    value={36}
                    sx={{ mt: 2, height: 8 }}
                    color="info"
                  />
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Grid>
      </Grid>

      {/* Detailed Metrics Dialog */}
      <Dialog
        open={fullscreenDialog}
        onClose={() => setFullscreenDialog(false)}
        maxWidth="lg"
        fullWidth
        fullScreen
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h5">Detailed Performance Analytics</Typography>
            <IconButton onClick={() => setFullscreenDialog(false)}>
              <CloseIcon />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, textAlign: 'center' }}>
                <TimelineIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>Time Series Analysis</Typography>
                <Typography color="text.secondary">
                  Interactive charts showing agent performance over time
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, textAlign: 'center' }}>
                <PieChartIcon sx={{ fontSize: 60, color: 'success.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>Resource Distribution</Typography>
                <Typography color="text.secondary">
                  Resource allocation across different agent types
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, textAlign: 'center' }}>
                <BarChartIcon sx={{ fontSize: 60, color: 'warning.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>Task Performance</Typography>
                <Typography color="text.secondary">
                  Comparative analysis of task completion rates
                </Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3, textAlign: 'center' }}>
                <ShowChartIcon sx={{ fontSize: 60, color: 'info.main', mb: 2 }} />
                <Typography variant="h6" gutterBottom>Trend Analysis</Typography>
                <Typography color="text.secondary">
                  Long-term trends and performance predictions
                </Typography>
              </Paper>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setFullscreenDialog(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AnalyticsDashboard;