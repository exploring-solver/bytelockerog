// src/components/dashboard/AlertsPanel.jsx
import React from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  List, 
  ListItem, 
  ListItemText,
  ListItemIcon,
  Chip,
  Box,
  IconButton,
  Collapse
} from '@mui/material';
import { 
  Warning,
  Error,
  Info,
  ExpandMore,
  ExpandLess,
  Person
} from '@mui/icons-material';
import { useState } from 'react';

const getSeverityIcon = (severity) => {
  switch (severity) {
    case 'high':
      return <Error color="error" />;
    case 'medium':
      return <Warning color="warning" />;
    default:
      return <Info color="info" />;
  }
};

const getSeverityColor = (severity) => {
  switch (severity) {
    case 'high':
      return 'error';
    case 'medium':
      return 'warning';
    default:
      return 'info';
  }
};

const AlertsPanel = ({ alerts }) => {
  const [expandedId, setExpandedId] = useState(null);

  const handleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id);
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Recent Alerts
        </Typography>
        <List>
          {alerts.map((alert) => (
            <React.Fragment key={alert.id}>
              <ListItem 
                divider 
                secondaryAction={
                  <IconButton onClick={() => handleExpand(alert.id)}>
                    {expandedId === alert.id ? <ExpandLess /> : <ExpandMore />}
                  </IconButton>
                }
              >
                <ListItemIcon>
                  {getSeverityIcon(alert.severity)}
                </ListItemIcon>
                <ListItemText
                  primary={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {alert.type}
                      <Chip 
                        label={alert.severity}
                        size="small"
                        color={getSeverityColor(alert.severity)}
                      />
                      {alert.resolved && (
                        <Chip 
                          label="Resolved"
                          size="small"
                          color="success"
                        />
                      )}
                    </Box>
                  }
                  secondary={`${new Date(alert.timestamp).toLocaleString()} - ${alert.location}`}
                />
              </ListItem>
              <Collapse in={expandedId === alert.id}>
                <Box sx={{ p: 2, bgcolor: 'action.hover' }}>
                  <Typography variant="body2" paragraph>
                    {alert.details}
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Person fontSize="small" />
                    <Typography variant="body2">
                      Detected: {alert.facesDetected.join(', ')}
                    </Typography>
                  </Box>
                </Box>
              </Collapse>
            </React.Fragment>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default AlertsPanel;