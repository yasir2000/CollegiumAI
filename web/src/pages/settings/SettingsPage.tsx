import React from 'react';
import { Box, Typography } from '@mui/material';

const SettingsPage: React.FC = () => (
  <Box>
    <Typography variant="h4" fontWeight="bold" gutterBottom>Settings</Typography>
    <Typography variant="subtitle1" color="text.secondary">System configuration and preferences</Typography>
  </Box>
);

export default SettingsPage;