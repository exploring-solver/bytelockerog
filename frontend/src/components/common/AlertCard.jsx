// src/components/common/AlertCard.jsx
import { Card, CardContent, Typography, Box, Chip } from '@mui/material';
import { Warning, Error, Info } from '@mui/icons-material';

const getAlertIcon = (severity) => {
  switch (severity) {
    case 'high':
      return <Error color="error" />;
    case 'medium':
      return <Warning color="warning" />;
    default:
      return <Info color="info" />;
  }
};

const AlertCard = ({ alert }) => {
  return (
    <Card sx={{ mb: 1 }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          {getAlertIcon(alert.severity)}
          <Typography variant="h6" sx={{ ml: 1 }}>
            {alert.title}
          </Typography>
          <Chip 
            label={alert.severity} 
            color={alert.severity === 'high' ? 'error' : 'warning'}
            size="small"
            sx={{ ml: 'auto' }}
          />
        </Box>
        <Typography variant="body2" color="text.secondary">
          {alert.description}
        </Typography>
        <Typography variant="caption" display="block" sx={{ mt: 1 }}>
          {new Date(alert.timestamp).toLocaleString()}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default AlertCard;