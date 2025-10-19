import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Grid,
  Button,
  Chip,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  ListItemIcon,
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
  Divider,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  LinearProgress,
  Alert,
  Badge
} from '@mui/material';
import {
  Person as PersonIcon,
  School as SchoolIcon,
  Assignment as AssignmentIcon,
  TrendingUp as TrendingUpIcon,
  Notifications as NotificationIcon,
  Event as EventIcon,
  Schedule as ScheduleIcon,
  Grade as GradeIcon,
  Message as MessageIcon,
  VideoCall as VideoCallIcon,
  Download as DownloadIcon,
  Upload as UploadIcon,
  Settings as SettingsIcon,
  Help as HelpIcon,
  Security as SecurityIcon,
  Analytics as AnalyticsIcon,
  Group as GroupIcon,
  Class as ClassIcon,
  MenuBook as BookIcon,
  LocalLibrary as LibraryIcon,
  Science as ScienceIcon,
  Computer as ComputerIcon,
  Psychology as AIIcon,
  Language as LanguageIcon,
  Business as BusinessIcon,
  AccountBalance as FinanceIcon,
  VerifiedUser as CredentialIcon,
  Public as GlobalIcon,
  Timeline as TimelineIcon,
  Assessment as ReportIcon,
  Dashboard as DashboardIcon,
  Speed as PerformanceIcon,
  Warning as WarningIcon,
  CheckCircle as SuccessIcon,
  Info as InfoIcon,
  Error as ErrorIcon
} from '@mui/icons-material';

interface UniversityDashboardProps {
  userRole?: 'student' | 'faculty' | 'admin' | 'staff';
}

const UniversityDashboard: React.FC<UniversityDashboardProps> = ({ userRole = 'student' }) => {
  const [selectedCourse, setSelectedCourse] = useState('');
  const [openCourseDialog, setOpenCourseDialog] = useState(false);
  const [notifications] = useState([
    { id: 1, type: 'assignment', title: 'Assignment Due Tomorrow', message: 'Machine Learning Project Submission', time: '2 hours ago', urgent: true },
    { id: 2, type: 'grade', title: 'Grade Released', message: 'Data Structures Exam - Grade: A-', time: '4 hours ago', urgent: false },
    { id: 3, type: 'event', title: 'Guest Lecture', message: 'AI Ethics - Prof. Sarah Johnson', time: '1 day ago', urgent: false },
    { id: 4, type: 'system', title: 'System Maintenance', message: 'Scheduled maintenance tonight 2-4 AM', time: '2 days ago', urgent: false }
  ]);

  const courses = [
    { id: 'CS401', name: 'Advanced Machine Learning', professor: 'Dr. Alan Smith', progress: 75, grade: 'A-', nextClass: 'Tomorrow 10:00 AM' },
    { id: 'CS302', name: 'Database Systems', professor: 'Dr. Maria Garcia', progress: 82, grade: 'B+', nextClass: 'Friday 2:00 PM' },
    { id: 'CS501', name: 'AI Ethics', professor: 'Dr. Sarah Johnson', progress: 60, grade: 'A', nextClass: 'Monday 9:00 AM' },
    { id: 'CS450', name: 'Software Engineering', professor: 'Dr. Robert Chen', progress: 88, grade: 'A-', nextClass: 'Wednesday 1:00 PM' }
  ];

  const upcomingEvents = [
    { id: 1, title: 'Research Symposium', date: '2024-10-25', time: '9:00 AM', location: 'Main Auditorium', type: 'conference' },
    { id: 2, title: 'Career Fair', date: '2024-10-28', time: '10:00 AM', location: 'Student Center', type: 'career' },
    { id: 3, title: 'Guest Lecture: Future of AI', date: '2024-10-30', time: '3:00 PM', location: 'CS Building Room 101', type: 'lecture' },
    { id: 4, title: 'Final Exam Period', date: '2024-11-15', time: 'All Day', location: 'Various Locations', type: 'exam' }
  ];

  const quickActions = [
    { name: 'Join Virtual Class', icon: <VideoCallIcon />, color: 'primary', action: () => console.log('Join class') },
    { name: 'Submit Assignment', icon: <UploadIcon />, color: 'success', action: () => console.log('Submit assignment') },
    { name: 'View Grades', icon: <GradeIcon />, color: 'info', action: () => console.log('View grades') },
    { name: 'Schedule Meeting', icon: <ScheduleIcon />, color: 'warning', action: () => console.log('Schedule meeting') }
  ];

  const academicProgress = {
    currentGPA: 3.7,
    completedCredits: 85,
    totalCredits: 120,
    expectedGraduation: 'Spring 2025'
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'assignment': return <AssignmentIcon color="warning" />;
      case 'grade': return <GradeIcon color="success" />;
      case 'event': return <EventIcon color="info" />;
      case 'system': return <SettingsIcon color="action" />;
      default: return <InfoIcon />;
    }
  };

  const getEventTypeColor = (type: string) => {
    switch (type) {
      case 'conference': return 'primary';
      case 'career': return 'success';
      case 'lecture': return 'info';
      case 'exam': return 'error';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* Welcome Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          Welcome back, {userRole === 'student' ? 'Alex' : 'Professor'}! 👋
        </Typography>
        <Typography variant="body1" color="text.secondary">
          {userRole === 'student' 
            ? 'Here\'s your academic dashboard with the latest updates and progress.'
            : 'Here\'s your faculty dashboard with course management and student information.'
          }
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Quick Actions */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <DashboardIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Quick Actions
              </Typography>
              <Grid container spacing={2}>
                {quickActions.map((action, index) => (
                  <Grid item xs={6} sm={3} key={index}>
                    <Button
                      variant="outlined"
                      fullWidth
                      startIcon={action.icon}
                      color={action.color as any}
                      onClick={action.action}
                      sx={{ py: 2 }}
                    >
                      {action.name}
                    </Button>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Academic Progress */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <TrendingUpIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Academic Progress
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">Current GPA</Typography>
                <Typography variant="h4" color="primary" fontWeight="bold">
                  {academicProgress.currentGPA}
                </Typography>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  Completed Credits: {academicProgress.completedCredits}/{academicProgress.totalCredits}
                </Typography>
                <LinearProgress 
                  variant="determinate" 
                  value={(academicProgress.completedCredits / academicProgress.totalCredits) * 100} 
                  sx={{ mt: 1, height: 8, borderRadius: 4 }}
                />
              </Box>
              <Chip 
                label={`Expected Graduation: ${academicProgress.expectedGraduation}`} 
                color="success" 
                icon={<SchoolIcon />}
              />
            </CardContent>
          </Card>
        </Grid>

        {/* Notifications */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <Badge badgeContent={notifications.filter(n => n.urgent).length} color="error">
                  <NotificationIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                </Badge>
                Recent Notifications
              </Typography>
              <List>
                {notifications.slice(0, 4).map((notification) => (
                  <ListItem key={notification.id} divider>
                    <ListItemAvatar>
                      <Avatar sx={{ bgcolor: notification.urgent ? 'error.main' : 'primary.main' }}>
                        {getNotificationIcon(notification.type)}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={notification.title}
                      secondary={
                        <Box>
                          <Typography variant="body2" color="text.secondary">
                            {notification.message}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {notification.time}
                          </Typography>
                        </Box>
                      }
                    />
                    {notification.urgent && (
                      <ListItemSecondaryAction>
                        <Chip label="Urgent" color="error" size="small" />
                      </ListItemSecondaryAction>
                    )}
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Current Courses */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <BookIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Current Courses
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Course</TableCell>
                      <TableCell>Professor</TableCell>
                      <TableCell>Progress</TableCell>
                      <TableCell>Grade</TableCell>
                      <TableCell>Next Class</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {courses.map((course) => (
                      <TableRow key={course.id} hover>
                        <TableCell>
                          <Typography variant="subtitle2">{course.name}</Typography>
                          <Typography variant="caption" color="text.secondary">
                            {course.id}
                          </Typography>
                        </TableCell>
                        <TableCell>{course.professor}</TableCell>
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
                        <TableCell>
                          <Chip 
                            label={course.grade} 
                            color={course.grade.startsWith('A') ? 'success' : 'primary'} 
                            size="small"
                          />
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">{course.nextClass}</Typography>
                        </TableCell>
                        <TableCell>
                          <Button
                            size="small"
                            variant="outlined"
                            onClick={() => {
                              setSelectedCourse(course.name);
                              setOpenCourseDialog(true);
                            }}
                          >
                            Details
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Upcoming Events */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <EventIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Upcoming Events
              </Typography>
              <List>
                {upcomingEvents.map((event) => (
                  <ListItem key={event.id} divider>
                    <ListItemText
                      primary={event.title}
                      secondary={
                        <Box>
                          <Typography variant="body2" color="text.secondary">
                            {event.date} at {event.time}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            📍 {event.location}
                          </Typography>
                        </Box>
                      }
                    />
                    <ListItemSecondaryAction>
                      <Chip 
                        label={event.type} 
                        color={getEventTypeColor(event.type) as any} 
                        size="small"
                      />
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Study Resources */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <LibraryIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Study Resources
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Button
                    variant="outlined"
                    fullWidth
                    startIcon={<ComputerIcon />}
                    onClick={() => console.log('Open LMS')}
                  >
                    Learning Management
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    variant="outlined"
                    fullWidth
                    startIcon={<LibraryIcon />}
                    onClick={() => console.log('Open library')}
                  >
                    Digital Library
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    variant="outlined"
                    fullWidth
                    startIcon={<AIIcon />}
                    onClick={() => console.log('Open AI tutor')}
                  >
                    AI Tutor
                  </Button>
                </Grid>
                <Grid item xs={6}>
                  <Button
                    variant="outlined"
                    fullWidth
                    startIcon={<GroupIcon />}
                    onClick={() => console.log('Join study group')}
                  >
                    Study Groups
                  </Button>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Course Details Dialog */}
      <Dialog open={openCourseDialog} onClose={() => setOpenCourseDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Course Details: {selectedCourse}</DialogTitle>
        <DialogContent>
          <Alert severity="info" sx={{ mb: 2 }}>
            <Typography variant="body2">
              Access comprehensive course information, assignments, grades, and resources.
            </Typography>
          </Alert>
          <Box sx={{ mt: 2 }}>
            <Typography variant="h6" gutterBottom>Course Information</Typography>
            <Typography variant="body2" paragraph>
              This course provides comprehensive coverage of advanced topics in the selected subject area.
              Students will engage with cutting-edge research and practical applications.
            </Typography>
            <Typography variant="h6" gutterBottom>Resources Available</Typography>
            <List dense>
              <ListItem>
                <ListItemIcon><VideoCallIcon /></ListItemIcon>
                <ListItemText primary="Virtual Classroom Access" />
              </ListItem>
              <ListItem>
                <ListItemIcon><DownloadIcon /></ListItemIcon>
                <ListItemText primary="Course Materials & Recordings" />
              </ListItem>
              <ListItem>
                <ListItemIcon><AssignmentIcon /></ListItemIcon>
                <ListItemText primary="Assignment Submission Portal" />
              </ListItem>
              <ListItem>
                <ListItemIcon><MessageIcon /></ListItemIcon>
                <ListItemText primary="Discussion Forums" />
              </ListItem>
            </List>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenCourseDialog(false)}>Close</Button>
          <Button variant="contained" onClick={() => setOpenCourseDialog(false)}>
            Access Course
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default UniversityDashboard;