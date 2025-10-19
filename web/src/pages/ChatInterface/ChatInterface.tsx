import React, { useState, useRef, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  TextField,
  Button,
  IconButton,
  Paper,
  Avatar,
  Chip,
  LinearProgress,
  Divider
} from '@mui/material';
import {
  Send as SendIcon,
  Clear as ClearIcon,
  Psychology as PsychologyIcon,
  AutoAwesome as AutoAwesomeIcon,
  Memory as MemoryIcon,
  Lightbulb as LightbulbIcon
} from '@mui/icons-material';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store/store';
import { addMessage, setLoading, ChatMessage } from '../../store/slices/chatSlice';

const ChatInterface: React.FC = () => {
  const dispatch = useDispatch();
  const { currentPersona } = useSelector((state: RootState) => state.persona);
  const { messages, isLoading } = useSelector((state: RootState) => state.chat);
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      content: inputMessage,
      role: 'user',
      timestamp: new Date(),
    };

    dispatch(addMessage(userMessage));
    setInputMessage('');
    dispatch(setLoading(true));

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: ChatMessage = {
        id: `ai-${Date.now()}`,
        content: `I understand you're asking about "${inputMessage}". As ${currentPersona?.name || 'an AI assistant'}, I can help you with this. This is a sophisticated response that would come from the CollegiumAI cognitive architecture, taking into account my persona's expertise and your specific needs.`,
        role: 'assistant',
        timestamp: new Date(),
        confidence: Math.random() * 0.3 + 0.7,
        cognitiveInsights: [
          'Applied semantic memory retrieval',
          'Engaged contextual reasoning',
          'Activated empathetic response patterns'
        ],
        agentInfo: currentPersona ? {
          name: currentPersona.name,
          type: currentPersona.type
        } : undefined
      };

      dispatch(addMessage(aiResponse));
      dispatch(setLoading(false));
    }, 2000);
  };

  const handleClearChat = () => {
    // Implementation would clear messages
  };

  return (
    <Container maxWidth="xl" sx={{ py: 4, height: 'calc(100vh - 64px)' }}>
      <Grid container spacing={3} sx={{ height: '100%' }}>
        {/* Chat Area */}
        <Grid item xs={12} md={8}>
          <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent sx={{ pb: 1 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h5" gutterBottom>
                  Chat with CollegiumAI
                </Typography>
                <IconButton onClick={handleClearChat}>
                  <ClearIcon />
                </IconButton>
              </Box>
              {currentPersona && (
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                  <Avatar sx={{ bgcolor: 'primary.main' }}>
                    {currentPersona.name.charAt(0)}
                  </Avatar>
                  <Box>
                    <Typography variant="body1">{currentPersona.name}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {currentPersona.description}
                    </Typography>
                  </Box>
                </Box>
              )}
            </CardContent>

            {/* Messages */}
            <Box sx={{ flexGrow: 1, overflow: 'auto', px: 2 }}>
              {messages.length === 0 ? (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <PsychologyIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="h6" color="text.secondary">
                    Start a conversation with CollegiumAI
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Ask questions, seek guidance, or explore the cognitive capabilities
                  </Typography>
                </Box>
              ) : (
                messages.map((message) => (
                  <Box
                    key={message.id}
                    sx={{
                      mb: 2,
                      display: 'flex',
                      justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start'
                    }}
                  >
                    <Paper
                      sx={{
                        p: 2,
                        maxWidth: '70%',
                        bgcolor: message.role === 'user' ? 'primary.main' : 'grey.100',
                        color: message.role === 'user' ? 'white' : 'text.primary'
                      }}
                    >
                      <Typography variant="body1">{message.content}</Typography>
                      {message.confidence && (
                        <Box sx={{ mt: 1 }}>
                          <Typography variant="caption" sx={{ opacity: 0.8 }}>
                            Confidence: {(message.confidence * 100).toFixed(1)}%
                          </Typography>
                        </Box>
                      )}
                      {message.cognitiveInsights && (
                        <Box sx={{ mt: 1 }}>
                          {message.cognitiveInsights.map((insight, index) => (
                            <Chip
                              key={index}
                              label={insight}
                              size="small"
                              sx={{ mr: 0.5, mb: 0.5 }}
                              variant="outlined"
                            />
                          ))}
                        </Box>
                      )}
                    </Paper>
                  </Box>
                ))
              )}
              {isLoading && (
                <Box sx={{ mb: 2 }}>
                  <Paper sx={{ p: 2, bgcolor: 'grey.100' }}>
                    <Typography variant="body2" sx={{ mb: 1 }}>
                      CollegiumAI is thinking...
                    </Typography>
                    <LinearProgress />
                  </Paper>
                </Box>
              )}
              <div ref={messagesEndRef} />
            </Box>

            {/* Input */}
            <Box sx={{ p: 2 }}>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <TextField
                  fullWidth
                  placeholder="Type your message..."
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  disabled={isLoading}
                />
                <Button
                  variant="contained"
                  onClick={handleSendMessage}
                  disabled={!inputMessage.trim() || isLoading}
                  sx={{ minWidth: 56 }}
                >
                  <SendIcon />
                </Button>
              </Box>
            </Box>
          </Card>
        </Grid>

        {/* Sidebar */}
        <Grid item xs={12} md={4}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, height: '100%' }}>
            {/* Cognitive Status */}
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  <AutoAwesomeIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Cognitive Status
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" gutterBottom>Processing Efficiency</Typography>
                  <LinearProgress variant="determinate" value={87} />
                  <Typography variant="caption" color="text.secondary">87%</Typography>
                </Box>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="body2" gutterBottom>Memory Utilization</Typography>
                  <LinearProgress variant="determinate" value={64} color="secondary" />
                  <Typography variant="caption" color="text.secondary">64%</Typography>
                </Box>
                <Box>
                  <Typography variant="body2" gutterBottom>Attention Focus</Typography>
                  <LinearProgress variant="determinate" value={92} color="success" />
                  <Typography variant="caption" color="text.secondary">92%</Typography>
                </Box>
              </CardContent>
            </Card>

            {/* Active Insights */}
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  <LightbulbIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Active Insights
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                  <Chip label="Pattern recognition active" size="small" color="primary" />
                  <Chip label="Context analysis engaged" size="small" color="secondary" />
                  <Chip label="Empathy protocols active" size="small" color="success" />
                </Box>
              </CardContent>
            </Card>

            {/* Memory Context */}
            <Card sx={{ flexGrow: 1 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  <MemoryIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Memory Context
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Recent conversation topics and learned patterns will appear here.
                </Typography>
                <Divider sx={{ my: 2 }} />
                <Typography variant="body2" color="text.secondary">
                  No previous context available.
                </Typography>
              </CardContent>
            </Card>
          </Box>
        </Grid>
      </Grid>
    </Container>
  );
};

export default ChatInterface;