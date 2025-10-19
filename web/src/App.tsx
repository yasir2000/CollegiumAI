import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';

// Import components
import Navigation from './components/Navigation/Navigation';
import Dashboard from './pages/Dashboard/Dashboard';
import PersonaGallery from './pages/PersonaGallery/PersonaGallery';
import ChatInterface from './pages/ChatInterface/ChatInterface';
import MultiAgentWorkspace from './pages/MultiAgentWorkspace/MultiAgentWorkspace';
import CognitiveMonitor from './pages/CognitiveMonitor/CognitiveMonitor';
import UniversitySystems from './pages/UniversitySystems/UniversitySystems';
import PerformanceAnalytics from './pages/PerformanceAnalytics/PerformanceAnalytics';
import SystemStatus from './components/SystemStatus/SystemStatus';

function App() {
  return (
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
  );
}

export default App;