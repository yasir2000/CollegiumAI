import React from 'react';
import { Container, Typography, Card, CardContent, Box, Grid } from '@mui/material';
import { School as SchoolIcon } from '@mui/icons-material';

const UniversitySystems: React.FC = () => {
  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom fontWeight="bold">
        University Systems Management
      </Typography>
      <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
        Comprehensive university management and support systems
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                <SchoolIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
                Digital University Platform
              </Typography>
              <Box sx={{ textAlign: 'center', py: 4 }}>
                <Typography variant="h6" color="text.secondary">
                  University Systems Coming Soon
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                  This platform will include academic support, research tools, 
                  administrative functions, and student services.
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default UniversitySystems;