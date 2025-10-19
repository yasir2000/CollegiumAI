import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { Provider } from 'react-redux';
import { store } from './store/store';

// Import components - We'll create these
import Navigation from './components/Navigation/Navigation';
import Dashboard from './pages/Dashboard/Dashboard';
import PersonaGallery from './pages/PersonaGallery/PersonaGallery';
import ChatInterface from './pages/ChatInterface/ChatInterface';
import MultiAgentWorkspace from './pages/MultiAgentWorkspace/MultiAgentWorkspace';
import CognitiveMonitor from './pages/CognitiveMonitor/CognitiveMonitor';
import UniversitySystems from './pages/UniversitySystems/UniversitySystems';
import PerformanceAnalytics from './pages/PerformanceAnalytics/PerformanceAnalytics';
import SystemStatus from './components/SystemStatus/SystemStatus';

// Create theme for CollegiumAI
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#dc004e',
      light: '#ff5983',
      dark: '#9a0036',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: 600,
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          borderRadius: 12,
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
          fontWeight: 500,
        },
      },
    },
  },
});

function App() {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <Navigation />
            <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/personas" element={<PersonaGallery />} />
                <Route path="/chat" element={<ChatInterface />} />
                <Route path="/multi-agent" element={<MultiAgentWorkspace />} />
                <Route path="/cognitive" element={<CognitiveMonitor />} />
                <Route path="/university" element={<UniversitySystems />} />
                <Route path="/analytics" element={<PerformanceAnalytics />} />
              </Routes>
            </Box>
            <SystemStatus />
          </Box>
        </Router>
      </ThemeProvider>
    </Provider>
  );
}

export default App;