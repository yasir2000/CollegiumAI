import React from 'react';
import { Box, Typography } from '@mui/material';

const ProfilePage: React.FC = () => (
  <Box>
    <Typography variant="h4" fontWeight="bold" gutterBottom>Profile</Typography>
    <Typography variant="subtitle1" color="text.secondary">User profile and account settings</Typography>
  </Box>
);

export default ProfilePage;