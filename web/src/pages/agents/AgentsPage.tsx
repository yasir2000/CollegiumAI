import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  TextField,
  Paper,
  Chip,
  Avatar,
  IconButton,
  Divider,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  SmartToy,
  Send,
  Add,
  Delete,
  School,
  Person,
  Public,
  AccountBalance,
  Psychology,
  Work,
} from '@mui/icons-material';
import { RootState, AppDispatch } from '../../store';
import {
  createSession,
  setActiveSession,
  addMessage,
  deleteSession,
} from '../../store/features/agents/agentSlice';

const agentTypes = [
  {
    id: 'academic_advisor',
    name: 'Academic Advisor',
    description: 'Helps students with course selection, degree planning, and academic guidance',
    icon: <School />,
    color: '#1976d2',
  },
  {
    id: 'student_services',
    name: 'Student Services',
    description: 'Assists with campus life, housing, dining, and student activities',
    icon: <Person />,
    color: '#dc004e',
  },
  {
    id: 'bologna_process',
    name: 'Bologna Process',
    description: 'Manages ECTS credits, mobility programs, and European qualifications',
    icon: <Public />,
    color: '#2e7d32',
  },
  {
    id: 'admissions',
    name: 'Admissions',
    description: 'Handles application processes, requirements, and enrollment procedures',
    icon: <AccountBalance />,
    color: '#ed6c02',
  },
  {
    id: 'career_services',
    name: 'Career Services',
    description: 'Provides career guidance, job search assistance, and internship opportunities',
    icon: <Work />,
    color: '#9c27b0',
  },
  {
    id: 'research_assistant',
    name: 'Research Assistant',
    description: 'Supports research activities, grant applications, and academic publications',
    icon: <Psychology />,
    color: '#00695c',
  },
];

const AgentsPage: React.FC = () => {
  const [newSessionDialog, setNewSessionDialog] = useState(false);
  const [selectedAgentType, setSelectedAgentType] = useState('');
  const [sessionTitle, setSessionTitle] = useState('');
  const [messageInput, setMessageInput] = useState('');

  const dispatch = useDispatch<AppDispatch>();
  const { sessions, activeSessionId, isLoading } = useSelector(
    (state: RootState) => state.agents
  );

  const activeSession = sessions.find(s => s.id === activeSessionId);

  const handleCreateSession = () => {
    if (selectedAgentType && sessionTitle.trim()) {
      dispatch(createSession({
        agentType: selectedAgentType,
        title: sessionTitle.trim(),
      }));
      setNewSessionDialog(false);
      setSelectedAgentType('');
      setSessionTitle('');
    }
  };

  const handleSendMessage = () => {
    if (messageInput.trim() && activeSessionId) {
      // Add user message
      dispatch(addMessage({
        sessionId: activeSessionId,
        message: {
          type: 'user',
          content: messageInput.trim(),
          timestamp: new Date(),
        },
      }));

      // Simulate agent response (in real app, this would call the API)
      setTimeout(() => {
        const agentType = activeSession?.agentType || 'academic_advisor';
        const agentInfo = agentTypes.find(a => a.id === agentType);
        
        dispatch(addMessage({
          sessionId: activeSessionId,
          message: {
            type: 'agent',
            content: `This is a simulated response from the ${agentInfo?.name || 'AI Agent'}. In the full implementation, this would connect to the CollegiumAI backend API to process your query using the ReACT framework and provide intelligent responses based on your university's context and governance frameworks.`,
            timestamp: new Date(),
            agentType,
          },
        }));
      }, 1500);

      setMessageInput('');
    }
  };

  const handleDeleteSession = (sessionId: string) => {
    dispatch(deleteSession(sessionId));
  };

  const getAgentInfo = (agentType: string) => {
    return agentTypes.find(a => a.id === agentType) || agentTypes[0];
  };

  return (
    <Box>
      <Box mb={4} display="flex" justifyContent="space-between" alignItems="center">
        <Box>
          <Typography variant="h4" fontWeight="bold">
            AI Agents
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Interact with specialized AI agents for different university services
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setNewSessionDialog(true)}
        >
          New Session
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* Sessions Sidebar */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Active Sessions
              </Typography>
              {sessions.length === 0 ? (
                <Box textAlign="center" py={4}>
                  <SmartToy sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                  <Typography color="text.secondary">
                    No active sessions. Create a new session to start chatting with AI agents.
                  </Typography>
                </Box>
              ) : (
                <List>
                  {sessions.map((session) => {
                    const agentInfo = getAgentInfo(session.agentType);
                    return (
                      <ListItem key={session.id} disablePadding>
                        <ListItemButton
                          selected={session.id === activeSessionId}
                          onClick={() => dispatch(setActiveSession(session.id))}
                        >
                          <Avatar
                            sx={{
                              bgcolor: agentInfo.color,
                              width: 32,
                              height: 32,
                              mr: 2,
                            }}
                          >
                            {agentInfo.icon}
                          </Avatar>
                          <ListItemText
                            primary={session.title}
                            secondary={`${agentInfo.name} • ${session.messages.length} messages`}
                          />
                          <IconButton
                            size="small"
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDeleteSession(session.id);
                            }}
                          >
                            <Delete fontSize="small" />
                          </IconButton>
                        </ListItemButton>
                      </ListItem>
                    );
                  })}
                </List>
              )}
            </CardContent>
          </Card>

          {/* Available Agents */}
          <Card sx={{ mt: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Available Agents
              </Typography>
              <Grid container spacing={1}>
                {agentTypes.map((agent) => (
                  <Grid item xs={12} key={agent.id}>
                    <Chip
                      icon={agent.icon}
                      label={agent.name}
                      variant="outlined"
                      sx={{
                        width: '100%',
                        justifyContent: 'flex-start',
                        mb: 1,
                        '& .MuiChip-icon': { color: agent.color },
                      }}
                    />
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Chat Area */}
        <Grid item xs={12} md={8}>
          <Card sx={{ height: '600px', display: 'flex', flexDirection: 'column' }}>
            {activeSession ? (
              <>
                {/* Chat Header */}
                <Box
                  p={2}
                  borderBottom={1}
                  borderColor="divider"
                  display="flex"
                  alignItems="center"
                >
                  <Avatar
                    sx={{
                      bgcolor: getAgentInfo(activeSession.agentType).color,
                      mr: 2,
                    }}
                  >
                    {getAgentInfo(activeSession.agentType).icon}
                  </Avatar>
                  <Box>
                    <Typography variant="h6">{activeSession.title}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {getAgentInfo(activeSession.agentType).name}
                    </Typography>
                  </Box>
                </Box>

                {/* Messages */}
                <Box flex={1} p={2} sx={{ overflowY: 'auto' }}>
                  {activeSession.messages.length === 0 ? (
                    <Box textAlign="center" py={4}>
                      <Typography color="text.secondary">
                        Start a conversation with the {getAgentInfo(activeSession.agentType).name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        {getAgentInfo(activeSession.agentType).description}
                      </Typography>
                    </Box>
                  ) : (
                    activeSession.messages.map((message) => (
                      <Box
                        key={message.id}
                        mb={2}
                        display="flex"
                        justifyContent={message.type === 'user' ? 'flex-end' : 'flex-start'}
                      >
                        <Paper
                          sx={{
                            p: 2,
                            maxWidth: '70%',
                            bgcolor: message.type === 'user' ? 'primary.main' : 'grey.100',
                            color: message.type === 'user' ? 'white' : 'text.primary',
                          }}
                        >
                          <Typography>{message.content}</Typography>
                          <Typography
                            variant="caption"
                            sx={{
                              opacity: 0.7,
                              mt: 1,
                              display: 'block',
                            }}
                          >
                            {new Date(message.timestamp).toLocaleTimeString()}
                          </Typography>
                        </Paper>
                      </Box>
                    ))
                  )}
                </Box>

                {/* Message Input */}
                <Box p={2} borderTop={1} borderColor="divider">
                  <Box display="flex" gap={1}>
                    <TextField
                      fullWidth
                      placeholder="Type your message..."
                      value={messageInput}
                      onChange={(e) => setMessageInput(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                      disabled={isLoading}
                    />
                    <Button
                      variant="contained"
                      onClick={handleSendMessage}
                      disabled={!messageInput.trim() || isLoading}
                      sx={{ minWidth: 'auto', px: 2 }}
                    >
                      <Send />
                    </Button>
                  </Box>
                </Box>
              </>
            ) : (
              <Box
                display="flex"
                alignItems="center"
                justifyContent="center"
                height="100%"
                flexDirection="column"
              >
                <SmartToy sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                <Typography variant="h6" color="text.secondary" gutterBottom>
                  Select a session to start chatting
                </Typography>
                <Typography color="text.secondary" textAlign="center">
                  Choose an existing session from the sidebar or create a new one to begin
                  interacting with our AI agents.
                </Typography>
              </Box>
            )}
          </Card>
        </Grid>
      </Grid>

      {/* New Session Dialog */}
      <Dialog open={newSessionDialog} onClose={() => setNewSessionDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create New Agent Session</DialogTitle>
        <DialogContent>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            Choose an AI agent type and provide a title for your session.
          </Typography>
          
          <Typography variant="subtitle2" sx={{ mt: 3, mb: 2 }}>
            Select Agent Type:
          </Typography>
          <Grid container spacing={2}>
            {agentTypes.map((agent) => (
              <Grid item xs={12} sm={6} key={agent.id}>
                <Card
                  sx={{
                    cursor: 'pointer',
                    border: selectedAgentType === agent.id ? 2 : 1,
                    borderColor: selectedAgentType === agent.id ? 'primary.main' : 'divider',
                  }}
                  onClick={() => setSelectedAgentType(agent.id)}
                >
                  <CardContent sx={{ p: 2 }}>
                    <Box display="flex" alignItems="center" mb={1}>
                      <Avatar sx={{ bgcolor: agent.color, width: 32, height: 32, mr: 1 }}>
                        {agent.icon}
                      </Avatar>
                      <Typography variant="subtitle2">{agent.name}</Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {agent.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          <TextField
            fullWidth
            label="Session Title"
            value={sessionTitle}
            onChange={(e) => setSessionTitle(e.target.value)}
            margin="normal"
            placeholder="e.g., Course Planning for Fall 2024"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setNewSessionDialog(false)}>Cancel</Button>
          <Button
            onClick={handleCreateSession}
            variant="contained"
            disabled={!selectedAgentType || !sessionTitle.trim()}
          >
            Create Session
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default AgentsPage;