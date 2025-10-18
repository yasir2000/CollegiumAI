import React from 'react';
import { Box, Paper, Typography, Container } from '@mui/material';
import { SmartToy } from '@mui/icons-material';

interface AuthLayoutProps {
  children: React.ReactNode;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children }) => {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #1976d2 0%, #42a5f5 100%)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 3,
      }}
    >
      <Container maxWidth="sm">
        <Paper
          elevation={24}
          sx={{
            padding: 4,
            borderRadius: 3,
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
          }}
        >
          {/* Logo and branding */}
          <Box
            display="flex"
            alignItems="center"
            justifyContent="center"
            mb={4}
          >
            <SmartToy 
              sx={{ 
                fontSize: 48, 
                color: 'primary.main', 
                mr: 2 
              }} 
            />
            <Box textAlign="center">
              <Typography
                variant="h4"
                component="h1"
                fontWeight="bold"
                color="primary.main"
              >
                CollegiumAI
              </Typography>
              <Typography
                variant="subtitle1"
                color="text.secondary"
                sx={{ mt: 1 }}
              >
                AI Multi-Agent Framework for Digital Universities
              </Typography>
            </Box>
          </Box>

          {/* Content */}
          {children}

          {/* Footer */}
          <Box textAlign="center" mt={4}>
            <Typography variant="body2" color="text.secondary">
              Powered by AI Multi-Agent Collaborative Framework
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
              Supporting AACSB, HEFCE, WASC, QAA & Bologna Process compliance
            </Typography>
          </Box>
        </Paper>
      </Container>
    </Box>
  );
};

export default AuthLayout;