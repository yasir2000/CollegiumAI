import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Avatar,
  Paper,
  Divider,
} from '@mui/material';
import {
  TrendingUp,
  School,
  Person,
  AccountBalance,
  SmartToy,
  Public,
  CheckCircle,
  Warning,
  Error,
  Timeline,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { RootState, AppDispatch } from '../../store';

// Mock data for demonstration
const mockStudentGrowthData = [
  { month: 'Jan', students: 12000, faculty: 450 },
  { month: 'Feb', students: 12500, faculty: 460 },
  { month: 'Mar', students: 13200, faculty: 475 },
  { month: 'Apr', students: 13800, faculty: 485 },
  { month: 'May', students: 14300, faculty: 495 },
  { month: 'Jun', students: 15000, faculty: 500 },
];

const mockCredentialData = [
  { name: 'Bachelor Degrees', value: 4500, color: '#1976d2' },
  { name: 'Master Degrees', value: 2800, color: '#42a5f5' },
  { name: 'Doctorate Degrees', value: 450, color: '#90caf9' },
  { name: 'Certificates', value: 1200, color: '#bbdefb' },
];

const mockComplianceData = [
  { framework: 'AACSB', status: 'compliant', score: 95 },
  { framework: 'WASC', status: 'compliant', score: 92 },
  { framework: 'Bologna Process', status: 'compliant', score: 88 },
  { framework: 'QAA', status: 'under_review', score: 85 },
];

const mockRecentActivities = [
  {
    id: 1,
    type: 'credential',
    message: 'New credential issued to María González',
    timestamp: '2 minutes ago',
    icon: <AccountBalance />,
  },
  {
    id: 2,
    type: 'agent',
    message: 'Bologna Process agent processed 15 mobility requests',
    timestamp: '15 minutes ago',
    icon: <SmartToy />,
  },
  {
    id: 3,
    type: 'compliance',
    message: 'AACSB compliance audit completed successfully',
    timestamp: '1 hour ago',
    icon: <CheckCircle />,
  },
  {
    id: 4,
    type: 'blockchain',
    message: 'Smart contract deployed for new governance framework',
    timestamp: '2 hours ago',
    icon: <AccountBalance />,
  },
];

const DashboardPage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { user } = useSelector((state: RootState) => state.auth);
  const { stats } = useSelector((state: RootState) => state.university);
  const { isConnected } = useSelector((state: RootState) => state.blockchain);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'compliant':
        return <CheckCircle color="success" />;
      case 'under_review':
        return <Warning color="warning" />;
      case 'non_compliant':
        return <Error color="error" />;
      default:
        return <Warning color="warning" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'compliant':
        return 'success';
      case 'under_review':
        return 'warning';
      case 'non_compliant':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      {/* Welcome Header */}
      <Box mb={4}>
        <Typography variant="h4" fontWeight="bold" color="text.primary">
          Welcome back, {user?.name || 'User'}
        </Typography>
        <Typography variant="subtitle1" color="text.secondary" sx={{ mt: 1 }}>
          Here's what's happening at your digital university today
        </Typography>
      </Box>

      {/* Key Metrics Cards */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Total Students
                  </Typography>
                  <Typography variant="h4" fontWeight="bold">
                    15,000
                  </Typography>
                  <Typography variant="body2" color="success.main">
                    +12% from last month
                  </Typography>
                </Box>
                <Avatar sx={{ bgcolor: 'primary.main', width: 56, height: 56 }}>
                  <School />
                </Avatar>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Faculty Members
                  </Typography>
                  <Typography variant="h4" fontWeight="bold">
                    500
                  </Typography>
                  <Typography variant="body2" color="success.main">
                    +8% from last month
                  </Typography>
                </Box>
                <Avatar sx={{ bgcolor: 'secondary.main', width: 56, height: 56 }}>
                  <Person />
                </Avatar>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    Credentials Issued
                  </Typography>
                  <Typography variant="h4" fontWeight="bold">
                    8,950
                  </Typography>
                  <Typography variant="body2" color="success.main">
                    +15% from last month
                  </Typography>
                </Box>
                <Avatar sx={{ bgcolor: 'success.main', width: 56, height: 56 }}>
                  <AccountBalance />
                </Avatar>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Box>
                  <Typography color="text.secondary" gutterBottom>
                    AI Agents Active
                  </Typography>
                  <Typography variant="h4" fontWeight="bold">
                    8
                  </Typography>
                  <Box display="flex" alignItems="center" mt={1}>
                    <Box
                      sx={{
                        width: 8,
                        height: 8,
                        borderRadius: '50%',
                        backgroundColor: isConnected ? 'success.main' : 'error.main',
                        mr: 1,
                      }}
                    />
                    <Typography variant="body2" color="text.secondary">
                      {isConnected ? 'All systems online' : 'Connection issues'}
                    </Typography>
                  </Box>
                </Box>
                <Avatar sx={{ bgcolor: 'info.main', width: 56, height: 56 }}>
                  <SmartToy />
                </Avatar>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts Row */}
      <Grid container spacing={3} mb={4}>
        {/* Growth Chart */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Student & Faculty Growth
              </Typography>
              <Box height={300}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={mockStudentGrowthData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="students" stroke="#1976d2" strokeWidth={2} />
                    <Line type="monotone" dataKey="faculty" stroke="#dc004e" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Credential Distribution */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Credential Distribution
              </Typography>
              <Box height={300}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={mockCredentialData}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    >
                      {mockCredentialData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Bottom Row */}
      <Grid container spacing={3}>
        {/* Compliance Status */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Governance Compliance Status
              </Typography>
              <List>
                {mockComplianceData.map((item, index) => (
                  <React.Fragment key={item.framework}>
                    <ListItem>
                      <ListItemIcon>
                        {getStatusIcon(item.status)}
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box display="flex" alignItems="center" justifyContent="space-between">
                            <Typography>{item.framework}</Typography>
                            <Chip
                              label={item.status.replace('_', ' ')}
                              size="small"
                              color={getStatusColor(item.status) as any}
                              variant="outlined"
                            />
                          </Box>
                        }
                        secondary={
                          <Box mt={1}>
                            <Box display="flex" alignItems="center" justifyContent="space-between">
                              <Typography variant="body2">Compliance Score</Typography>
                              <Typography variant="body2">{item.score}%</Typography>
                            </Box>
                            <LinearProgress
                              variant="determinate"
                              value={item.score}
                              sx={{ mt: 1 }}
                              color={item.score >= 90 ? 'success' : item.score >= 75 ? 'warning' : 'error'}
                            />
                          </Box>
                        }
                      />
                    </ListItem>
                    {index < mockComplianceData.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Activity
              </Typography>
              <List>
                {mockRecentActivities.map((activity, index) => (
                  <React.Fragment key={activity.id}>
                    <ListItem>
                      <ListItemIcon>
                        <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
                          {activity.icon}
                        </Avatar>
                      </ListItemIcon>
                      <ListItemText
                        primary={activity.message}
                        secondary={activity.timestamp}
                      />
                    </ListItem>
                    {index < mockRecentActivities.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DashboardPage;