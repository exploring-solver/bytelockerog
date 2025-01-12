import React from 'react';
import { Box, Typography, Grid, Paper } from '@mui/material';
import CameraGrid from '../components/dashboard/CameraGrid';
import AlertsPanel from '../components/dashboard/AlertsPanel';

const SecurityView = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3 }}>
        Security Monitoring
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} lg={8}>
          <Paper elevation={3} sx={{ p: 2, height: 'calc(100vh - 180px)', overflow: 'auto' }}>
            <CameraGrid viewMode="grid" />
          </Paper>
        </Grid>
        <Grid item xs={12} lg={4}>
          <AlertsPanel alerts={[]} />
        </Grid>
      </Grid>
    </Box>
  );
};

export default SecurityView;