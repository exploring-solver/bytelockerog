import { Card, CardContent, Typography, Box } from '@mui/material';

const MetricCard = ({ title, value, icon, color }) => {
  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          {icon}
          <Typography variant="h6" sx={{ ml: 1 }}>
            {title}
          </Typography>
        </Box>
        <Typography 
          variant="h4" 
          sx={{ color: `${color}.main` }}
        >
          {value}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default MetricCard;