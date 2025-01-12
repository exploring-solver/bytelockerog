// src/components/dashboard/MetricsPanel.jsx
import React from 'react';
import { Card, CardContent, Typography, Box, Grid, LinearProgress } from '@mui/material';
import { 
  People, 
  Warning, 
  DensityMedium, 
  TrendingUp, 
  AccessTime,
  SecurityOutlined 
} from '@mui/icons-material';

const MetricsPanel = ({ metrics }) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Metrics Overview
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <People sx={{ mr: 1, color: 'primary.main' }} />
              <Box>
                <Typography variant="body2" color="text.secondary">
                  Total People
                </Typography>
                <Typography variant="h6">
                  {metrics.totalPeople.toLocaleString()}
                </Typography>
              </Box>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <DensityMedium sx={{ mr: 1, color: 'warning.main' }} />
              <Box>
                <Typography variant="body2" color="text.secondary">
                  Current Density
                </Typography>
                <Typography variant="h6">
                  {(metrics.crowdDensity * 100).toFixed(1)}%
                </Typography>
              </Box>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Warning sx={{ mr: 1, color: 'error.main' }} />
              <Box>
                <Typography variant="body2" color="text.secondary">
                  Active Alerts
                </Typography>
                <Typography variant="h6">
                  {metrics.alerts.length}
                </Typography>
              </Box>
            </Box>
          </Grid>

          <Grid item xs={12} md={6}>
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" color="text.secondary">
                Safety Score
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={metrics.safetyScore} 
                color={metrics.safetyScore > 80 ? "success" : "warning"}
                sx={{ height: 10, borderRadius: 5 }}
              />
              <Typography variant="body2" align="right">
                {metrics.safetyScore}%
              </Typography>
            </Box>
          </Grid>

          <Grid item xs={12} md={6}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <AccessTime sx={{ mr: 1, color: 'info.main' }} />
              <Box>
                <Typography variant="body2" color="text.secondary">
                  Peak Hour
                </Typography>
                <Typography variant="h6">
                  {metrics.peakHour}:00
                </Typography>
              </Box>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default MetricsPanel;