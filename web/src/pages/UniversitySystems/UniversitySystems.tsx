import React, { useState } from 'react';
import {
  Container,
  Typography,
  Card,
  CardContent,
  Box,
  Grid,
  Tab,
  Tabs,
  Paper,
  Button,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  LinearProgress,
  Badge,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
  AlertTitle
} from '@mui/material';
import {
  School as SchoolIcon,
  Dashboard as DashboardIcon,
  People as PeopleIcon,
  MenuBook as CourseIcon,
  Timeline as AnalyticsIcon,
  Settings as SettingsIcon,
  Notifications as NotificationIcon,
  LocalLibrary as LibraryIcon,
  Security as SecurityIcon,
  TrendingUp as TrendingUpIcon,
  Assessment as ReportsIcon,
  Person as PersonIcon,
  Grade as GradeIcon,
  LocalLibrary as ResearchIcon,
  Psychology as AIIcon,
  AccountBalance as FinanceIcon,
  VerifiedUser as CredentialIcon,
  Public as GlobalIcon,
  Science as ScienceIcon,
  Computer as TechIcon,
  Groups as CollaborationIcon,
  VideoCall as VideoIcon,
  Chat as ChatIcon,
  Warning as WarningIcon,
  CheckCircle as SuccessIcon,
  Info as InfoIcon
} from '@mui/icons-material';

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
      id={`university-tabpanel-${index}`}
      aria-labelledby={`university-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const UniversitySystems: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [notifications] = useState(12);
  const [systemHealth] = useState(98.5);
  const [activeUsers] = useState(2847);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedFeature, setSelectedFeature] = useState('');

  // Mock data for demonstration
  const universityStats = {
    totalStudents: 15420,
    totalFaculty: 892,
    totalCourses: 1247,
    researchProjects: 156,
    publications: 2341,
    graduationRate: 94.2,
    employmentRate: 89.7,
    satisfactionScore: 4.6
  };

  const recentActivities = [
    { id: 1, type: 'enrollment', message: 'New student enrollment: 47 students', time: '2 hours ago', severity: 'success' },
    { id: 2, type: 'research', message: 'Research grant approved: $2.3M for AI in Education', time: '4 hours ago', severity: 'info' },
    { id: 3, type: 'system', message: 'System maintenance scheduled for tomorrow', time: '6 hours ago', severity: 'warning' },
    { id: 4, type: 'academic', message: 'Final grades published for Fall 2024', time: '1 day ago', severity: 'success' },
    { id: 5, type: 'event', message: 'Virtual conference: Future of Education', time: '2 days ago', severity: 'info' }
  ];

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleFeatureClick = (feature: string) => {
    setSelectedFeature(feature);
    setOpenDialog(true);
  };

  const universityFeatures = [
    {
      category: 'Academic Management',
      features: [
        { name: 'Course Management', icon: <CourseIcon />, description: 'Comprehensive course planning and management', status: 'active' },
        { name: 'Student Information System', icon: <PersonIcon />, description: 'Complete student lifecycle management', status: 'active' },
        { name: 'Faculty Portal', icon: <PeopleIcon />, description: 'Faculty resources and collaboration tools', status: 'active' },
        { name: 'Grade Management', icon: <GradeIcon />, description: 'Automated grading and assessment tools', status: 'active' }
      ]
    },
    {
      category: 'Research & Innovation',
      features: [
        { name: 'Research Management', icon: <ResearchIcon />, description: 'Research project tracking and collaboration', status: 'active' },
        { name: 'AI Research Hub', icon: <AIIcon />, description: 'Advanced AI research and development platform', status: 'beta' },
        { name: 'Publication Management', icon: <LibraryIcon />, description: 'Academic publication and citation tracking', status: 'active' },
        { name: 'Lab Equipment Booking', icon: <ScienceIcon />, description: 'Laboratory resource management', status: 'active' }
      ]
    },
    {
      category: 'Digital Infrastructure',
      features: [
        { name: 'Learning Management System', icon: <TechIcon />, description: 'Comprehensive online learning platform', status: 'active' },
        { name: 'Virtual Collaboration', icon: <CollaborationIcon />, description: 'Real-time collaboration tools', status: 'active' },
        { name: 'Video Conferencing', icon: <VideoIcon />, description: 'Integrated video communication platform', status: 'active' },
        { name: 'AI Chat Support', icon: <ChatIcon />, description: '24/7 AI-powered student support', status: 'active' }
      ]
    },
    {
      category: 'Administrative Services',
      features: [
        { name: 'Financial Management', icon: <FinanceIcon />, description: 'Comprehensive financial tracking and reporting', status: 'active' },
        { name: 'Credential Verification', icon: <CredentialIcon />, description: 'Blockchain-based credential management', status: 'active' },
        { name: 'Global Partnerships', icon: <GlobalIcon />, description: 'International collaboration management', status: 'active' },
        { name: 'Security Center', icon: <SecurityIcon />, description: 'Advanced cybersecurity monitoring', status: 'active' }
      ]
    }
  ];

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h3" component="h1" gutterBottom fontWeight="bold">
            <SchoolIcon sx={{ mr: 2, fontSize: 40, verticalAlign: 'middle' }} />
            University Management System
          </Typography>
          <Typography variant="h6" color="text.secondary">
            Comprehensive digital university platform powered by AI
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Badge badgeContent={notifications} color="error">
            <IconButton>
              <NotificationIcon />
            </IconButton>
          </Badge>
          <Chip 
            label={`System Health: ${systemHealth}%`} 
            color="success" 
            icon={<SuccessIcon />}
          />
          <Chip 
            label={`${activeUsers} Active Users`} 
            color="primary" 
            icon={<PeopleIcon />}
          />
        </Box>
      </Box>

      {/* System Overview Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)' }}>
            <CardContent sx={{ color: 'white' }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                  <Typography variant="h4" fontWeight="bold">
                    {universityStats.totalStudents.toLocaleString()}
                  </Typography>
                  <Typography variant="body2">Total Students</Typography>
                </Box>
                <PersonIcon sx={{ fontSize: 40, opacity: 0.8 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #FF6B6B 30%, #FF8E8E 90%)' }}>
            <CardContent sx={{ color: 'white' }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                  <Typography variant="h4" fontWeight="bold">
                    {universityStats.totalFaculty}
                  </Typography>
                  <Typography variant="body2">Faculty Members</Typography>
                </Box>
                <PeopleIcon sx={{ fontSize: 40, opacity: 0.8 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #4ECDC4 30%, #44A08D 90%)' }}>
            <CardContent sx={{ color: 'white' }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                  <Typography variant="h4" fontWeight="bold">
                    {universityStats.totalCourses}
                  </Typography>
                  <Typography variant="body2">Active Courses</Typography>
                </Box>
                <CourseIcon sx={{ fontSize: 40, opacity: 0.8 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #A8E6CF 30%, #7FCDCD 90%)' }}>
            <CardContent sx={{ color: 'white' }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Box>
                  <Typography variant="h4" fontWeight="bold">
                    {universityStats.researchProjects}
                  </Typography>
                  <Typography variant="body2">Research Projects</Typography>
                </Box>
                <ResearchIcon sx={{ fontSize: 40, opacity: 0.8 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Main Tabs Interface */}
      <Paper sx={{ width: '100%' }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
          aria-label="university management tabs"
        >
          <Tab icon={<DashboardIcon />} label="Dashboard" />
          <Tab icon={<SchoolIcon />} label="Academic" />
          <Tab icon={<ResearchIcon />} label="Research" />
          <Tab icon={<PeopleIcon />} label="Community" />
          <Tab icon={<AnalyticsIcon />} label="Analytics" />
          <Tab icon={<SettingsIcon />} label="Administration" />
        </Tabs>

        {/* Dashboard Tab */}
        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <TrendingUpIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    University Performance Metrics
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">Graduation Rate</Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                        <LinearProgress 
                          variant="determinate" 
                          value={universityStats.graduationRate} 
                          sx={{ flexGrow: 1, mr: 2 }} 
                        />
                        <Typography variant="body2">{universityStats.graduationRate}%</Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="text.secondary">Employment Rate</Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                        <LinearProgress 
                          variant="determinate" 
                          value={universityStats.employmentRate} 
                          sx={{ flexGrow: 1, mr: 2 }} 
                        />
                        <Typography variant="body2">{universityStats.employmentRate}%</Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={12}>
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                        Student Satisfaction Score: {universityStats.satisfactionScore}/5.0
                      </Typography>
                      <LinearProgress 
                        variant="determinate" 
                        value={universityStats.satisfactionScore * 20} 
                        sx={{ mt: 1 }} 
                      />
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <NotificationIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Recent Activities
                  </Typography>
                  <List dense>
                    {recentActivities.map((activity) => (
                      <ListItem key={activity.id}>
                        <ListItemIcon>
                          {activity.severity === 'success' && <SuccessIcon color="success" />}
                          {activity.severity === 'warning' && <WarningIcon color="warning" />}
                          {activity.severity === 'info' && <InfoIcon color="info" />}
                        </ListItemIcon>
                        <ListItemText 
                          primary={activity.message}
                          secondary={activity.time}
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Academic Tab */}
        <TabPanel value={tabValue} index={1}>
          <Grid container spacing={3}>
            {universityFeatures.find(cat => cat.category === 'Academic Management')?.features.map((feature, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card 
                  sx={{ 
                    cursor: 'pointer', 
                    transition: 'transform 0.2s',
                    '&:hover': { transform: 'translateY(-4px)' }
                  }}
                  onClick={() => handleFeatureClick(feature.name)}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      {feature.icon}
                      <Typography variant="h6" sx={{ ml: 1 }}>
                        {feature.name}
                      </Typography>
                      <Chip 
                        label={feature.status} 
                        size="small" 
                        color={feature.status === 'active' ? 'success' : 'warning'}
                        sx={{ ml: 'auto' }}
                      />
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {feature.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>

        {/* Research Tab */}
        <TabPanel value={tabValue} index={2}>
          <Grid container spacing={3}>
            {universityFeatures.find(cat => cat.category === 'Research & Innovation')?.features.map((feature, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card 
                  sx={{ 
                    cursor: 'pointer', 
                    transition: 'transform 0.2s',
                    '&:hover': { transform: 'translateY(-4px)' }
                  }}
                  onClick={() => handleFeatureClick(feature.name)}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      {feature.icon}
                      <Typography variant="h6" sx={{ ml: 1 }}>
                        {feature.name}
                      </Typography>
                      <Chip 
                        label={feature.status} 
                        size="small" 
                        color={feature.status === 'active' ? 'success' : 'info'}
                        sx={{ ml: 'auto' }}
                      />
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {feature.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>

        {/* Community Tab */}
        <TabPanel value={tabValue} index={3}>
          <Grid container spacing={3}>
            {universityFeatures.find(cat => cat.category === 'Digital Infrastructure')?.features.map((feature, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card 
                  sx={{ 
                    cursor: 'pointer', 
                    transition: 'transform 0.2s',
                    '&:hover': { transform: 'translateY(-4px)' }
                  }}
                  onClick={() => handleFeatureClick(feature.name)}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      {feature.icon}
                      <Typography variant="h6" sx={{ ml: 1 }}>
                        {feature.name}
                      </Typography>
                      <Chip 
                        label={feature.status} 
                        size="small" 
                        color="success"
                        sx={{ ml: 'auto' }}
                      />
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {feature.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>

        {/* Analytics Tab */}
        <TabPanel value={tabValue} index={4}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <ReportsIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    University Analytics Dashboard
                  </Typography>
                  <TableContainer>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Metric</TableCell>
                          <TableCell align="right">Current Value</TableCell>
                          <TableCell align="right">Target</TableCell>
                          <TableCell align="right">Progress</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        <TableRow>
                          <TableCell>Student Enrollment</TableCell>
                          <TableCell align="right">{universityStats.totalStudents.toLocaleString()}</TableCell>
                          <TableCell align="right">16,000</TableCell>
                          <TableCell align="right">96.4%</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Research Publications</TableCell>
                          <TableCell align="right">{universityStats.publications}</TableCell>
                          <TableCell align="right">2,500</TableCell>
                          <TableCell align="right">93.6%</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>Faculty Satisfaction</TableCell>
                          <TableCell align="right">4.3/5.0</TableCell>
                          <TableCell align="right">4.5/5.0</TableCell>
                          <TableCell align="right">95.6%</TableCell>
                        </TableRow>
                        <TableRow>
                          <TableCell>System Uptime</TableCell>
                          <TableCell align="right">99.7%</TableCell>
                          <TableCell align="right">99.9%</TableCell>
                          <TableCell align="right">99.8%</TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Administration Tab */}
        <TabPanel value={tabValue} index={5}>
          <Grid container spacing={3}>
            {universityFeatures.find(cat => cat.category === 'Administrative Services')?.features.map((feature, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Card 
                  sx={{ 
                    cursor: 'pointer', 
                    transition: 'transform 0.2s',
                    '&:hover': { transform: 'translateY(-4px)' }
                  }}
                  onClick={() => handleFeatureClick(feature.name)}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      {feature.icon}
                      <Typography variant="h6" sx={{ ml: 1 }}>
                        {feature.name}
                      </Typography>
                      <Chip 
                        label={feature.status} 
                        size="small" 
                        color="success"
                        sx={{ ml: 'auto' }}
                      />
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {feature.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>
      </Paper>

      {/* Feature Detail Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {selectedFeature}
        </DialogTitle>
        <DialogContent>
          <Alert severity="info" sx={{ mb: 2 }}>
            <AlertTitle>Feature Information</AlertTitle>
            This feature is part of the comprehensive CollegiumAI university management system.
          </Alert>
          <Typography variant="body1" paragraph>
            {selectedFeature} provides advanced functionality for university operations and management.
            This feature integrates with the broader CollegiumAI ecosystem to provide:
          </Typography>
          <Typography variant="body2" component="ul">
            <li>Real-time data processing and analytics</li>
            <li>AI-powered insights and recommendations</li>
            <li>Seamless integration with existing university systems</li>
            <li>Advanced security and compliance features</li>
            <li>Mobile-responsive interface for accessibility</li>
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Close</Button>
          <Button variant="contained" onClick={() => setOpenDialog(false)}>
            Learn More
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default UniversitySystems;