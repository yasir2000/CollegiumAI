import React from 'react';
import { Box, Typography, Card, CardContent, Grid, Chip } from '@mui/material';
import { Public, School, AccountBalance } from '@mui/icons-material';

const BolognaProcessPage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Bologna Process
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" paragraph>
        European Higher Education Area compliance and ECTS management
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <Public color="primary" sx={{ mr: 2 }} />
                <Typography variant="h6">ECTS Credits</Typography>
              </Box>
              <Typography variant="h3" color="primary.main" gutterBottom>
                180,000
              </Typography>
              <Typography color="text.secondary">
                Total ECTS credits managed
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <School color="secondary" sx={{ mr: 2 }} />
                <Typography variant="h6">Mobility Programs</Typography>
              </Box>
              <Typography variant="h3" color="secondary.main" gutterBottom>
                45
              </Typography>
              <Typography color="text.secondary">
                Active Erasmus+ partnerships
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" mb={2}>
                <AccountBalance color="success" sx={{ mr: 2 }} />
                <Typography variant="h6">Recognition Rate</Typography>
              </Box>
              <Typography variant="h3" color="success.main" gutterBottom>
                98%
              </Typography>
              <Typography color="text.secondary">
                Automatic recognition success
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default BolognaProcessPage;