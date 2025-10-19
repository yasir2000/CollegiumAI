import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Grid,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Chip,
  TextField,
  Paper,
  Divider,
  IconButton,
  Badge,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Tab,
  Tabs,
  InputAdornment,
  Alert
} from '@mui/material';
import {
  Message as MessageIcon,
  Send as SendIcon,
  Search as SearchIcon,
  Filter as FilterIcon,
  Refresh as RefreshIcon,
  Psychology as PsychologyIcon,
  Engineering as EngineeringIcon,
  School as SchoolIcon,
  Security as SecurityIcon,
  Assessment as AssessmentIcon,
  Groups as GroupsIcon,
  Notifications as NotificationsIcon,
  Warning as WarningIcon,
  Info as InfoIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Close as CloseIcon
} from '@mui/icons-material';

interface Message {
  id: string;
  fromAgent: string;
  toAgent: string;
  content: string;
  timestamp: string;
  type: 'info' | 'request' | 'response' | 'alert' | 'error' | 'success';
  priority: 'low' | 'medium' | 'high' | 'critical';
  read: boolean;
  threadId?: string;
}

interface Agent {
  id: string;
  name: string;
  type: string;
  status: 'online' | 'busy' | 'offline';
  avatar: string;
  lastSeen: string;
}

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
      id={`comm-tabpanel-${index}`}
      aria-labelledby={`comm-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 0 }}>{children}</Box>}
    </div>
  );
}

const CommunicationHub: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);
  const [messageText, setMessageText] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [broadcastDialog, setBroadcastDialog] = useState(false);
  const [broadcastMessage, setBroadcastMessage] = useState('');

  const agents: Agent[] = [
    {
      id: 'agent-001',
      name: 'Alpha Research Agent',
      type: 'Research',
      status: 'online',
      avatar: 'AR',
      lastSeen: 'now'
    },
    {
      id: 'agent-002',
      name: 'Beta Engineering Agent',
      type: 'Engineering',
      status: 'busy',
      avatar: 'BE',
      lastSeen: '2 min ago'
    },
    {
      id: 'agent-003',
      name: 'Gamma Analytics Agent',
      type: 'Analytics',
      status: 'online',
      avatar: 'GA',
      lastSeen: 'now'
    },
    {
      id: 'agent-004',
      name: 'Delta Communication Agent',
      type: 'Communication',
      status: 'online',
      avatar: 'DC',
      lastSeen: 'now'
    },
    {
      id: 'agent-005',
      name: 'Epsilon Security Agent',
      type: 'Security',
      status: 'offline',
      avatar: 'ES',
      lastSeen: '1 hour ago'
    }
  ];

  const [messages] = useState<Message[]>([
    {
      id: 'msg-001',
      fromAgent: 'agent-001',
      toAgent: 'agent-002',
      content: 'Research findings are ready for implementation review. The analysis shows promising results for the new algorithm approach.',
      timestamp: '2025-10-19T15:30:00Z',
      type: 'info',
      priority: 'medium',
      read: true,
      threadId: 'thread-001'
    },
    {
      id: 'msg-002',
      fromAgent: 'agent-002',
      toAgent: 'agent-001',
      content: 'Received. Starting code implementation based on your research. ETA for initial prototype: 2 hours.',
      timestamp: '2025-10-19T15:32:00Z',
      type: 'response',
      priority: 'medium',
      read: true,
      threadId: 'thread-001'
    },
    {
      id: 'msg-003',
      fromAgent: 'agent-004',
      toAgent: 'all',
      content: 'System maintenance scheduled for tonight at 2:00 AM. All agents will be temporarily offline for 30 minutes.',
      timestamp: '2025-10-19T15:25:00Z',
      type: 'alert',
      priority: 'high',
      read: false
    },
    {
      id: 'msg-004',
      fromAgent: 'agent-005',
      toAgent: 'agent-004',
      content: 'Security audit complete. No vulnerabilities detected in the current communication protocols.',
      timestamp: '2025-10-19T15:20:00Z',
      type: 'success',
      priority: 'low',
      read: true
    },
    {
      id: 'msg-005',
      fromAgent: 'agent-003',
      toAgent: 'agent-002',
      content: 'Performance metrics analysis shows 15% improvement in processing speed. Detailed report attached.',
      timestamp: '2025-10-19T15:15:00Z',
      type: 'info',
      priority: 'medium',
      read: false
    }
  ]);

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
      case 'online': return 'success';
      case 'busy': return 'warning';
      case 'offline': return 'error';
      default: return 'default';
    }
  };

  const getMessageIcon = (type: string) => {
    switch (type) {
      case 'info': return <InfoIcon color="info" />;
      case 'request': return <MessageIcon color="primary" />;
      case 'response': return <CheckCircleIcon color="success" />;
      case 'alert': return <WarningIcon color="warning" />;
      case 'error': return <ErrorIcon color="error" />;
      case 'success': return <CheckCircleIcon color="success" />;
      default: return <MessageIcon />;
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

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleSendMessage = () => {
    if (messageText.trim() && selectedAgent) {
      // Add message sending logic here
      setMessageText('');
    }
  };

  const handleBroadcast = () => {
    if (broadcastMessage.trim()) {
      // Add broadcast logic here
      setBroadcastMessage('');
      setBroadcastDialog(false);
    }
  };

  const filteredMessages = messages.filter(msg =>
    msg.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
    agents.find(a => a.id === msg.fromAgent)?.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const unreadCount = messages.filter(msg => !msg.read).length;

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5" fontWeight="bold">
          <MessageIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
          Communication Hub
        </Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button
            variant="contained"
            startIcon={<GroupsIcon />}
            onClick={() => setBroadcastDialog(true)}
          >
            Broadcast
          </Button>
          <IconButton>
            <RefreshIcon />
          </IconButton>
        </Box>
      </Box>

      {/* Quick Stats */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center', py: 2 }}>
              <Badge badgeContent={unreadCount} color="error">
                <MessageIcon sx={{ fontSize: 32, color: 'primary.main' }} />
              </Badge>
              <Typography variant="h6" sx={{ mt: 1 }}>
                {messages.length}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Total Messages
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center', py: 2 }}>
              <GroupsIcon sx={{ fontSize: 32, color: 'success.main' }} />
              <Typography variant="h6" sx={{ mt: 1 }}>
                {agents.filter(a => a.status === 'online').length}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Online Agents
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center', py: 2 }}>
              <WarningIcon sx={{ fontSize: 32, color: 'warning.main' }} />
              <Typography variant="h6" sx={{ mt: 1 }}>
                {messages.filter(m => m.priority === 'high' || m.priority === 'critical').length}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                High Priority
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center', py: 2 }}>
              <NotificationsIcon sx={{ fontSize: 32, color: 'info.main' }} />
              <Typography variant="h6" sx={{ mt: 1 }}>
                {unreadCount}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                Unread Messages
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        {/* Agent List */}
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '600px', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
              <Typography variant="h6" gutterBottom>
                Active Agents
              </Typography>
              <List sx={{ flexGrow: 1, overflow: 'auto' }}>
                {agents.map((agent) => (
                  <ListItem
                    key={agent.id}
                    button
                    selected={selectedAgent === agent.id}
                    onClick={() => setSelectedAgent(agent.id)}
                    sx={{ borderRadius: 1, mb: 0.5 }}
                  >
                    <ListItemAvatar>
                      <Badge
                        variant="dot"
                        color={getStatusColor(agent.status) as any}
                        overlap="circular"
                        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                      >
                        <Avatar sx={{ bgcolor: 'primary.main' }}>
                          {getAgentIcon(agent.type)}
                        </Avatar>
                      </Badge>
                    </ListItemAvatar>
                    <ListItemText
                      primary={agent.name}
                      secondary={
                        <Box>
                          <Typography variant="caption" color="text.secondary">
                            {agent.type} • {agent.lastSeen}
                          </Typography>
                          <br />
                          <Chip
                            label={agent.status}
                            size="small"
                            color={getStatusColor(agent.status) as any}
                          />
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Communication Panel */}
        <Grid item xs={12} md={8}>
          <Card sx={{ height: '600px', display: 'flex', flexDirection: 'column' }}>
            <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
              <Tabs value={tabValue} onChange={handleTabChange}>
                <Tab label="All Messages" />
                <Tab label="Direct Messages" />
                <Tab label="Broadcasts" />
                <Tab label="Alerts" />
              </Tabs>
            </Box>

            <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', p: 0 }}>
              {/* Search Bar */}
              <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
                <TextField
                  fullWidth
                  placeholder="Search messages..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <SearchIcon />
                      </InputAdornment>
                    ),
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton size="small">
                          <FilterIcon />
                        </IconButton>
                      </InputAdornment>
                    )
                  }}
                  size="small"
                />
              </Box>

              {/* Messages */}
              <TabPanel value={tabValue} index={0}>
                <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
                  {filteredMessages.map((message) => {
                    const fromAgent = agents.find(a => a.id === message.fromAgent);
                    const toAgent = agents.find(a => a.id === message.toAgent);
                    return (
                      <Paper
                        key={message.id}
                        sx={{
                          p: 2,
                          mb: 2,
                          bgcolor: message.read ? 'background.paper' : 'action.hover'
                        }}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'start', gap: 2 }}>
                          <Avatar sx={{ bgcolor: 'primary.main' }}>
                            {fromAgent?.avatar || '?'}
                          </Avatar>
                          <Box sx={{ flexGrow: 1 }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                              <Typography variant="subtitle2">
                                {fromAgent?.name} → {message.toAgent === 'all' ? 'All Agents' : toAgent?.name}
                              </Typography>
                              {getMessageIcon(message.type)}
                              <Chip
                                label={message.priority}
                                size="small"
                                color={getPriorityColor(message.priority) as any}
                              />
                              <Typography variant="caption" color="text.secondary">
                                {new Date(message.timestamp).toLocaleString()}
                              </Typography>
                            </Box>
                            <Typography variant="body2">
                              {message.content}
                            </Typography>
                          </Box>
                        </Box>
                      </Paper>
                    );
                  })}
                </Box>
              </TabPanel>

              <TabPanel value={tabValue} index={1}>
                <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
                  {filteredMessages.filter(m => m.toAgent !== 'all').map((message) => {
                    const fromAgent = agents.find(a => a.id === message.fromAgent);
                    const toAgent = agents.find(a => a.id === message.toAgent);
                    return (
                      <Paper key={message.id} sx={{ p: 2, mb: 2 }}>
                        <Box sx={{ display: 'flex', alignItems: 'start', gap: 2 }}>
                          <Avatar sx={{ bgcolor: 'primary.main' }}>
                            {fromAgent?.avatar || '?'}
                          </Avatar>
                          <Box sx={{ flexGrow: 1 }}>
                            <Typography variant="subtitle2" gutterBottom>
                              {fromAgent?.name} → {toAgent?.name}
                            </Typography>
                            <Typography variant="body2">
                              {message.content}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {new Date(message.timestamp).toLocaleString()}
                            </Typography>
                          </Box>
                        </Box>
                      </Paper>
                    );
                  })}
                </Box>
              </TabPanel>

              <TabPanel value={tabValue} index={2}>
                <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
                  {filteredMessages.filter(m => m.toAgent === 'all').map((message) => {
                    const fromAgent = agents.find(a => a.id === message.fromAgent);
                    return (
                      <Alert
                        key={message.id}
                        severity={message.type === 'alert' ? 'warning' : 'info'}
                        sx={{ mb: 2 }}
                      >
                        <Typography variant="subtitle2" gutterBottom>
                          Broadcast from {fromAgent?.name}
                        </Typography>
                        <Typography variant="body2">
                          {message.content}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {new Date(message.timestamp).toLocaleString()}
                        </Typography>
                      </Alert>
                    );
                  })}
                </Box>
              </TabPanel>

              <TabPanel value={tabValue} index={3}>
                <Box sx={{ flexGrow: 1, overflow: 'auto', p: 2 }}>
                  {filteredMessages.filter(m => m.type === 'alert' || m.type === 'error').map((message) => {
                    const fromAgent = agents.find(a => a.id === message.fromAgent);
                    return (
                      <Alert
                        key={message.id}
                        severity={message.type === 'error' ? 'error' : 'warning'}
                        sx={{ mb: 2 }}
                      >
                        <Typography variant="subtitle2" gutterBottom>
                          Alert from {fromAgent?.name}
                        </Typography>
                        <Typography variant="body2">
                          {message.content}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {new Date(message.timestamp).toLocaleString()}
                        </Typography>
                      </Alert>
                    );
                  })}
                </Box>
              </TabPanel>

              {/* Message Input */}
              <Divider />
              <Box sx={{ p: 2 }}>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <TextField
                    fullWidth
                    placeholder={selectedAgent ? `Message to ${agents.find(a => a.id === selectedAgent)?.name}...` : 'Select an agent to send message...'}
                    value={messageText}
                    onChange={(e) => setMessageText(e.target.value)}
                    disabled={!selectedAgent}
                    multiline
                    maxRows={3}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleSendMessage();
                      }
                    }}
                  />
                  <Button
                    variant="contained"
                    onClick={handleSendMessage}
                    disabled={!selectedAgent || !messageText.trim()}
                    sx={{ minWidth: 'auto', px: 2 }}
                  >
                    <SendIcon />
                  </Button>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Broadcast Dialog */}
      <Dialog open={broadcastDialog} onClose={() => setBroadcastDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          Broadcast Message to All Agents
          <IconButton
            onClick={() => setBroadcastDialog(false)}
            sx={{ position: 'absolute', right: 8, top: 8 }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          <TextField
            fullWidth
            placeholder="Enter broadcast message..."
            value={broadcastMessage}
            onChange={(e) => setBroadcastMessage(e.target.value)}
            multiline
            rows={4}
            sx={{ mt: 2 }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setBroadcastDialog(false)}>Cancel</Button>
          <Button
            variant="contained"
            onClick={handleBroadcast}
            disabled={!broadcastMessage.trim()}
            startIcon={<SendIcon />}
          >
            Broadcast
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default CommunicationHub;