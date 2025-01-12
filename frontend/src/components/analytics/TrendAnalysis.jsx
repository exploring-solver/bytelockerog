// src/components/analytics/TrendAnalysis.jsx
import React from 'react';
import { Box, Typography } from '@mui/material';
import { Line } from 'react-chartjs-2';

const TrendAnalysis = () => {
  const data = {
    labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    datasets: [
      {
        label: 'Anomalies Detected',
        data: [2, 3, 1, 4, 2],
        fill: false,
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgba(255, 99, 132, 0.2)',
      },
    ],
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Weekly Anomaly Trends
      </Typography>
      <Line data={data} />
    </Box>
  );
};

export default TrendAnalysis;