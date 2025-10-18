import React from 'react';
import { Box, Typography, Card, CardContent, Grid, Button, Chip } from '@mui/material';
import { AccountBalance, CheckCircle, Warning, Error } from '@mui/icons-material';

const BlockchainPage: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" fontWeight="bold" gutterBottom>
        Blockchain & Credentials
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" paragraph>
        Manage blockchain credentials, smart contracts, and network status
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Network Status
              </Typography>
              <Box display="flex" alignItems="center" mb={2}>
                <CheckCircle color="success" sx={{ mr: 1 }} />
                <Typography>Connected to Ethereum Network</Typography>
              </Box>
              <Typography color="text.secondary">
                Block: 18,234,567 | Gas Price: 25 gwei
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Credentials Issued
              </Typography>
              <Typography variant="h3" color="primary.main" gutterBottom>
                8,950
              </Typography>
              <Typography color="text.secondary">
                Total verified credentials on blockchain
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default BlockchainPage;