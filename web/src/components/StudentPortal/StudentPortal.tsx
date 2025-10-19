import React, { useState } from 'react';
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Avatar,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Tab,
  Tabs,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Badge,
  IconButton,
  Alert
} from '@mui/material';
import {
  School as SchoolIcon,
  Assignment as AssignmentIcon,
  Grade as GradeIcon,
  Event as EventIcon,
  VideoCall as VideoCallIcon,
  Download as DownloadIcon,
  Upload as UploadIcon,
  Message as MessageIcon,
  LocalLibrary as LibraryIcon,
  Schedule as ScheduleIcon,
  Notifications as NotificationIcon,
  Settings as SettingsIcon,
  Dashboard as DashboardIcon,
  MenuBook as BookIcon,
  Person as PersonIcon,
  Email as EmailIcon,
  Phone as PhoneIcon,
  CalendarToday as CalendarIcon,
  TrendingUp as TrendingUpIcon,
  EmojiEvents as CertificateIcon,
  Verified as VerifiedIcon
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
      id={`student-tabpanel-${index}`}
      aria-labelledby={`student-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const StudentPortal: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [openAssignmentDialog, setOpenAssignmentDialog] = useState(false);
  const [selectedAssignment, setSelectedAssignment] = useState('');

  const studentInfo = {
    name: 'Alex Johnson',
    id: 'ST20241001',
    email: 'alex.johnson@university.edu',
    phone: '+1 (555) 123-4567',
    program: 'Bachelor of Science in Computer Science',
    year: 'Senior',
    semester: 'Fall 2024',
    gpa: 3.75,
    credits: 108,
    totalCredits: 120,
    expectedGraduation: 'Spring 2025',
    advisor: 'Dr. Sarah Wilson'
  };

  const currentCourses = [
    {
      id: 'CS401',
      name: 'Advanced Machine Learning',
      professor: 'Dr. Alan Smith',
      credits: 3,
      schedule: 'MWF 10:00-11:00 AM',
      progress: 75,
      grade: 'A-'
    },
    {
      id: 'CS450',
      name: 'Software Engineering',
      professor: 'Dr. Robert Chen',
      credits: 4,
      schedule: 'TTh 2:00-3:30 PM',
      progress: 88,
      grade: 'A'
    },
    {
      id: 'CS501',
      name: 'AI Ethics',
      professor: 'Dr. Sarah Johnson',
      credits: 3,
      schedule: 'MW 1:00-2:30 PM',
      progress: 60,
      grade: 'B+'
    }
  ];

  const assignments = [
    {
      id: 1,
      course: 'CS401',
      title: 'Neural Network Implementation',
      dueDate: '2024-10-25',
      status: 'pending',
      priority: 'high',
      description: 'Implement a deep neural network for image classification'
    },
    {
      id: 2,
      course: 'CS450',
      title: 'Project Design Document',
      dueDate: '2024-10-28',
      status: 'in-progress',
      priority: 'medium',
      description: 'Create comprehensive design document for final project'
    },
    {
      id: 3,
      course: 'CS501',
      title: 'Ethics Case Study Analysis',
      dueDate: '2024-11-02',
      status: 'not-started',
      priority: 'low',
      description: 'Analyze ethical implications of AI in healthcare'
    }
  ];

  const upcomingEvents = [
    {
      id: 1,
      title: 'Career Fair',
      date: '2024-10-28',
      time: '10:00 AM - 4:00 PM',
      location: 'Student Center',
      type: 'career'
    },
    {
      id: 2,
      title: 'Guest Lecture: Future of AI',
      date: '2024-10-30',
      time: '3:00 PM - 4:30 PM',
      location: 'CS Building Room 101',
      type: 'academic'
    },
    {
      id: 3,
      title: 'Study Group - Machine Learning',
      date: '2024-10-24',
      time: '7:00 PM - 9:00 PM',
      location: 'Library Room 205',
      type: 'study'
    }
  ];

  const achievements = [
    { name: 'Dean\'s List', semester: 'Spring 2024', description: 'GPA above 3.5' },
    { name: 'Research Excellence Award', semester: 'Fall 2023', description: 'Outstanding research contribution' },
    { name: 'Hackathon Winner', semester: 'Fall 2023', description: 'First place in university hackathon' }
  ];

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const getAssignmentStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'success';
      case 'in-progress': return 'warning';
      case 'pending': return 'error';
      default: return 'default';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Avatar sx={{ width: 60, height: 60, mr: 2, bgcolor: 'primary.main' }}>
            <PersonIcon sx={{ fontSize: 30 }} />
          </Avatar>
          <Box>
            <Typography variant="h4" fontWeight="bold">
              {studentInfo.name}
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              {studentInfo.program} • {studentInfo.year}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Student ID: {studentInfo.id} • GPA: {studentInfo.gpa}
            </Typography>
          </Box>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Badge badgeContent={3} color="error">
            <IconButton>
              <NotificationIcon />
            </IconButton>
          </Badge>
          <IconButton>
            <SettingsIcon />
          </IconButton>
        </Box>
      </Box>

      {/* Quick Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)' }}>
            <CardContent sx={{ color: 'white', textAlign: 'center' }}>
              <TrendingUpIcon sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" fontWeight="bold">
                {studentInfo.gpa}
              </Typography>
              <Typography variant="body2">Current GPA</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #4CAF50 30%, #81C784 90%)' }}>
            <CardContent sx={{ color: 'white', textAlign: 'center' }}>
              <BookIcon sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" fontWeight="bold">
                {currentCourses.length}
              </Typography>
              <Typography variant="body2">Current Courses</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #FF9800 30%, #FFB74D 90%)' }}>
            <CardContent sx={{ color: 'white', textAlign: 'center' }}>
              <AssignmentIcon sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" fontWeight="bold">
                {assignments.filter(a => a.status !== 'completed').length}
              </Typography>
              <Typography variant="body2">Pending Assignments</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ background: 'linear-gradient(45deg, #9C27B0 30%, #BA68C8 90%)' }}>
            <CardContent sx={{ color: 'white', textAlign: 'center' }}>
              <SchoolIcon sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h4" fontWeight="bold">
                {Math.round((studentInfo.credits / studentInfo.totalCredits) * 100)}%
              </Typography>
              <Typography variant="body2">Degree Progress</Typography>
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
          <Tab icon={<DashboardIcon />} label="Dashboard" />
          <Tab icon={<BookIcon />} label="Courses" />
          <Tab icon={<AssignmentIcon />} label="Assignments" />
          <Tab icon={<GradeIcon />} label="Grades" />
          <Tab icon={<EventIcon />} label="Calendar" />
          <Tab icon={<PersonIcon />} label="Profile" />
        </Tabs>

        {/* Dashboard Tab */}
        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <AssignmentIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Upcoming Assignments
                  </Typography>
                  <List>
                    {assignments.slice(0, 3).map((assignment) => (
                      <ListItem key={assignment.id} divider>
                        <ListItemIcon>
                          <AssignmentIcon color={getPriorityColor(assignment.priority) as any} />
                        </ListItemIcon>
                        <ListItemText
                          primary={assignment.title}
                          secondary={
                            <Box>
                              <Typography variant="body2">
                                {assignment.course} • Due: {assignment.dueDate}
                              </Typography>
                              <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                                <Chip 
                                  label={assignment.status} 
                                  size="small" 
                                  color={getAssignmentStatusColor(assignment.status) as any}
                                />
                                <Chip 
                                  label={assignment.priority} 
                                  size="small" 
                                  color={getPriorityColor(assignment.priority) as any}
                                />
                              </Box>
                            </Box>
                          }
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card sx={{ mb: 2 }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <EventIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Upcoming Events
                  </Typography>
                  <List dense>
                    {upcomingEvents.slice(0, 3).map((event) => (
                      <ListItem key={event.id}>
                        <ListItemText
                          primary={event.title}
                          secondary={`${event.date} • ${event.time}`}
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <CertificateIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Recent Achievements
                  </Typography>
                  <List dense>
                    {achievements.slice(0, 2).map((achievement, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <VerifiedIcon color="success" />
                        </ListItemIcon>
                        <ListItemText
                          primary={achievement.name}
                          secondary={achievement.semester}
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Courses Tab */}
        <TabPanel value={tabValue} index={1}>
          <Grid container spacing={3}>
            {currentCourses.map((course) => (
              <Grid item xs={12} md={6} key={course.id}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                      <Box>
                        <Typography variant="h6">{course.name}</Typography>
                        <Typography variant="body2" color="text.secondary">
                          {course.id} • {course.professor}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {course.credits} Credits • {course.schedule}
                        </Typography>
                      </Box>
                      <Chip 
                        label={course.grade} 
                        color={course.grade.startsWith('A') ? 'success' : 'primary'}
                      />
                    </Box>
                    <Box sx={{ mb: 2 }}>
                      <Typography variant="body2" color="text.secondary">
                        Progress: {course.progress}%
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={course.progress}
                        sx={{ mt: 1, height: 8, borderRadius: 4 }}
                      />
                    </Box>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                      <Button size="small" startIcon={<VideoCallIcon />}>
                        Join Class
                      </Button>
                      <Button size="small" startIcon={<MessageIcon />}>
                        Discussions
                      </Button>
                      <Button size="small" startIcon={<LibraryIcon />}>
                        Resources
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </TabPanel>

        {/* Assignments Tab */}
        <TabPanel value={tabValue} index={2}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Assignment Management
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Assignment</TableCell>
                      <TableCell>Course</TableCell>
                      <TableCell>Due Date</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Priority</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {assignments.map((assignment) => (
                      <TableRow key={assignment.id} hover>
                        <TableCell>
                          <Typography variant="subtitle2">{assignment.title}</Typography>
                        </TableCell>
                        <TableCell>{assignment.course}</TableCell>
                        <TableCell>{assignment.dueDate}</TableCell>
                        <TableCell>
                          <Chip 
                            label={assignment.status} 
                            size="small" 
                            color={getAssignmentStatusColor(assignment.status) as any}
                          />
                        </TableCell>
                        <TableCell>
                          <Chip 
                            label={assignment.priority} 
                            size="small" 
                            color={getPriorityColor(assignment.priority) as any}
                          />
                        </TableCell>
                        <TableCell>
                          <Button
                            size="small"
                            variant="outlined"
                            onClick={() => {
                              setSelectedAssignment(assignment.title);
                              setOpenAssignmentDialog(true);
                            }}
                          >
                            View Details
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </TabPanel>

        {/* Grades Tab */}
        <TabPanel value={tabValue} index={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Course Grades
                  </Typography>
                  <TableContainer>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Course</TableCell>
                          <TableCell>Current Grade</TableCell>
                          <TableCell>Credits</TableCell>
                          <TableCell>Progress</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {currentCourses.map((course) => (
                          <TableRow key={course.id}>
                            <TableCell>
                              <Typography variant="subtitle2">{course.name}</Typography>
                              <Typography variant="caption" color="text.secondary">
                                {course.id}
                              </Typography>
                            </TableCell>
                            <TableCell>
                              <Chip 
                                label={course.grade} 
                                color={course.grade.startsWith('A') ? 'success' : 'primary'}
                              />
                            </TableCell>
                            <TableCell>{course.credits}</TableCell>
                            <TableCell>
                              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                                <LinearProgress
                                  variant="determinate"
                                  value={course.progress}
                                  sx={{ width: 100, mr: 1 }}
                                />
                                <Typography variant="body2">{course.progress}%</Typography>
                              </Box>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Academic Summary
                  </Typography>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" color="text.secondary">Current GPA</Typography>
                    <Typography variant="h4" color="primary" fontWeight="bold">
                      {studentInfo.gpa}
                    </Typography>
                  </Box>
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" color="text.secondary">
                      Completed Credits: {studentInfo.credits}/{studentInfo.totalCredits}
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={(studentInfo.credits / studentInfo.totalCredits) * 100} 
                      sx={{ mt: 1, height: 8, borderRadius: 4 }}
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    Expected Graduation: {studentInfo.expectedGraduation}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Calendar Tab */}
        <TabPanel value={tabValue} index={4}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <CalendarIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Upcoming Events & Schedule
                  </Typography>
                  <List>
                    {upcomingEvents.map((event) => (
                      <ListItem key={event.id} divider>
                        <ListItemIcon>
                          <EventIcon color="primary" />
                        </ListItemIcon>
                        <ListItemText
                          primary={event.title}
                          secondary={
                            <Box>
                              <Typography variant="body2">
                                📅 {event.date} • ⏰ {event.time}
                              </Typography>
                              <Typography variant="body2">
                                📍 {event.location}
                              </Typography>
                            </Box>
                          }
                        />
                        <Chip label={event.type} size="small" />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    <ScheduleIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                    Class Schedule
                  </Typography>
                  <List dense>
                    {currentCourses.map((course) => (
                      <ListItem key={course.id}>
                        <ListItemText
                          primary={course.name}
                          secondary={course.schedule}
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Profile Tab */}
        <TabPanel value={tabValue} index={5}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Card>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Avatar sx={{ width: 100, height: 100, mx: 'auto', mb: 2, bgcolor: 'primary.main' }}>
                    <PersonIcon sx={{ fontSize: 50 }} />
                  </Avatar>
                  <Typography variant="h5" fontWeight="bold" gutterBottom>
                    {studentInfo.name}
                  </Typography>
                  <Typography variant="body1" color="text.secondary" gutterBottom>
                    {studentInfo.program}
                  </Typography>
                  <Chip label={studentInfo.year} color="primary" />
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} md={8}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Personal Information
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <PersonIcon sx={{ mr: 1, color: 'text.secondary' }} />
                        <Box>
                          <Typography variant="body2" color="text.secondary">Student ID</Typography>
                          <Typography variant="body1">{studentInfo.id}</Typography>
                        </Box>
                      </Box>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <EmailIcon sx={{ mr: 1, color: 'text.secondary' }} />
                        <Box>
                          <Typography variant="body2" color="text.secondary">Email</Typography>
                          <Typography variant="body1">{studentInfo.email}</Typography>
                        </Box>
                      </Box>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <PhoneIcon sx={{ mr: 1, color: 'text.secondary' }} />
                        <Box>
                          <Typography variant="body2" color="text.secondary">Phone</Typography>
                          <Typography variant="body1">{studentInfo.phone}</Typography>
                        </Box>
                      </Box>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                        <PersonIcon sx={{ mr: 1, color: 'text.secondary' }} />
                        <Box>
                          <Typography variant="body2" color="text.secondary">Academic Advisor</Typography>
                          <Typography variant="body1">{studentInfo.advisor}</Typography>
                        </Box>
                      </Box>
                    </Grid>
                  </Grid>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </TabPanel>
      </Paper>

      {/* Assignment Details Dialog */}
      <Dialog open={openAssignmentDialog} onClose={() => setOpenAssignmentDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Assignment Details: {selectedAssignment}</DialogTitle>
        <DialogContent>
          <Alert severity="info" sx={{ mb: 2 }}>
            Access assignment details, submission portal, and related resources.
          </Alert>
          <Typography variant="body1" paragraph>
            Complete assignment information including requirements, submission guidelines, and grading rubric.
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
            <Button variant="outlined" startIcon={<DownloadIcon />}>
              Download Materials
            </Button>
            <Button variant="outlined" startIcon={<UploadIcon />}>
              Submit Assignment
            </Button>
            <Button variant="outlined" startIcon={<MessageIcon />}>
              Ask Questions
            </Button>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenAssignmentDialog(false)}>Close</Button>
          <Button variant="contained" onClick={() => setOpenAssignmentDialog(false)}>
            Start Working
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default StudentPortal;