// src/components/analytics/ViolationChart.jsx
import React from 'react';
import { Box, Typography } from '@mui/material';
import { Bar } from 'react-chartjs-2';

const ViolationChart = () => {
  const data = {
    labels: ['Proximity', 'Unauthorized Access', 'Unsafe Behavior'],
    datasets: [
      {
        label: 'Violations',
        data: [12, 19, 3],
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Safety Violations
      </Typography>
      <Bar data={data} />
    </Box>
  );
};

export default ViolationChart;