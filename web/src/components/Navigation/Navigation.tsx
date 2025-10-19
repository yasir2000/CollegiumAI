import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Box, 
  Button, 
  IconButton,
  Badge,
  Menu,
  MenuItem,
  Avatar,
  Chip
} from '@mui/material';
import { 
  Notifications as NotificationsIcon,
  Psychology as PsychologyIcon,
  School as SchoolIcon,
  Groups as GroupsIcon,
  Analytics as AnalyticsIcon,
  Chat as ChatIcon,
  Dashboard as DashboardIcon,
  Memory as MemoryIcon
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { RootState } from '../../store/store';

const Navigation: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { currentPersona } = useSelector((state: RootState) => state.persona);
  const { alerts } = useSelector((state: RootState) => state.system);
  const { isOnline } = useSelector((state: RootState) => state.system);

  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

  const handleNotificationClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleNotificationClose = () => {
    setAnchorEl(null);
  };

  const navigationItems = [
    { path: '/', label: 'Dashboard', icon: <DashboardIcon /> },
    { path: '/personas', label: 'Personas', icon: <SchoolIcon /> },
    { path: '/chat', label: 'Chat', icon: <ChatIcon /> },
    { path: '/multi-agent', label: 'Multi-Agent', icon: <GroupsIcon /> },
    { path: '/cognitive', label: 'Cognitive', icon: <MemoryIcon /> },
    { path: '/university', label: 'University', icon: <PsychologyIcon /> },
    { path: '/analytics', label: 'Analytics', icon: <AnalyticsIcon /> },
  ];

  const unreadAlerts = alerts.filter(alert => !alert.dismissed).length;

  return (
    <AppBar position="static" elevation={2}>
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
          <SchoolIcon sx={{ mr: 2, color: 'inherit' }} />
          <Typography variant="h6" component="div" sx={{ fontWeight: 600 }}>
            CollegiumAI
          </Typography>
          <Chip
            label={isOnline ? 'Online' : 'Offline'}
            color={isOnline ? 'success' : 'error'}
            size="small"
            sx={{ ml: 2 }}
          />
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {navigationItems.map((item) => (
            <Button
              key={item.path}
              color="inherit"
              startIcon={item.icon}
              onClick={() => navigate(item.path)}
              sx={{
                backgroundColor: location.pathname === item.path ? 'rgba(255,255,255,0.1)' : 'transparent',
                '&:hover': {
                  backgroundColor: 'rgba(255,255,255,0.2)',
                },
              }}
            >
              {item.label}
            </Button>
          ))}

          <IconButton
            color="inherit"
            onClick={handleNotificationClick}
            sx={{ ml: 2 }}
          >
            <Badge badgeContent={unreadAlerts} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>

          {currentPersona && (
            <Box sx={{ display: 'flex', alignItems: 'center', ml: 2 }}>
              <Avatar sx={{ width: 32, height: 32, mr: 1, bgcolor: 'secondary.main' }}>
                {currentPersona.name.charAt(0)}
              </Avatar>
              <Box>
                <Typography variant="body2" sx={{ fontSize: '0.8rem' }}>
                  {currentPersona.name}
                </Typography>
                <Typography variant="caption" sx={{ fontSize: '0.7rem', opacity: 0.8 }}>
                  {currentPersona.type}
                </Typography>
              </Box>
            </Box>
          )}
        </Box>

        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleNotificationClose}
          PaperProps={{
            style: {
              maxHeight: 300,
              width: 300,
            },
          }}
        >
          {alerts.slice(0, 5).map((alert) => (
            <MenuItem key={alert.id} onClick={handleNotificationClose}>
              <Box>
                <Typography variant="body2" fontWeight="bold">
                  {alert.title}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {alert.message}
                </Typography>
              </Box>
            </MenuItem>
          ))}
          {alerts.length === 0 && (
            <MenuItem onClick={handleNotificationClose}>
              <Typography variant="body2" color="text.secondary">
                No new notifications
              </Typography>
            </MenuItem>
          )}
        </Menu>
      </Toolbar>
    </AppBar>
  );
};

export default Navigation;