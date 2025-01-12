import React from 'react';
import { Box, Typography } from '@mui/material';
import { Line } from 'react-chartjs-2';

const DensityGraph = () => {
  const data = {
    labels: ['10:00', '11:00', '12:00', '13:00', '14:00'],
    datasets: [
      {
        label: 'Crowd Density',
        data: [0.2, 0.3, 0.5, 0.4, 0.6],
        fill: false,
        backgroundColor: 'rgb(75, 192, 192)',
        borderColor: 'rgba(75, 192, 192, 0.2)',
      },
    ],
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Crowd Density Over Time
      </Typography>
      <Line data={data} />
    </Box>
  );
};

export default DensityGraph;