// src/pages/Analytics.jsx
import React from 'react';
import { Box, Typography, Grid, Paper } from '@mui/material';
import DensityGraph from '../components/analytics/DensityGraph';
import ViolationChart from '../components/analytics/ViolationChart';
import TrendAnalysis from '../components/analytics/TrendAnalysis';
import AnomaliesList from '../components/analytics/AnomaliesList';
import { CategoryScale, Chart, registerables } from 'chart.js';

Chart.register(CategoryScale);
Chart.register(...registerables);

const Analytics = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3 }}>
        Analytics Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 2 }}>
            <DensityGraph />
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 2 }}>
            <ViolationChart />
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ p: 2 }}>
            <TrendAnalysis />
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ p: 2 }}>
            <AnomaliesList />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Analytics;