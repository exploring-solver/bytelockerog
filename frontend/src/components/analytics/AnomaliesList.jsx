import React, { useState } from 'react';
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Collapse,
  Divider,
} from '@mui/material';
import { ExpandMore, ExpandLess } from '@mui/icons-material';

const mockAnomalies = [
  {
    id: 1,
    type: 'Unauthorized Access',
    timestamp: '2023-10-01T10:15:00',
    details: 'Person detected in restricted area',
    facesDetected: ['John Doe', 'Jane Smith'],
  },
  {
    id: 2,
    type: 'Proximity Alert',
    timestamp: '2023-10-01T11:00:00',
    details: 'Multiple people detected in close proximity',
    facesDetected: ['Alice Johnson'],
  },
  {
    id: 3,
    type: 'Loitering',
    timestamp: '2023-10-01T12:30:00',
    details: 'Person loitering near entrance for over 10 minutes',
    facesDetected: ['Unknown'],
  },
  // Add more mock anomalies as needed
];

const AnomaliesList = () => {
  const [expanded, setExpanded] = useState(null);

  const handleToggle = (id) => {
    setExpanded(expanded === id ? null : id);
  };

  return (
    <Box>
      <Typography variant="h6" sx={{ mb: 2 }}>
        Detected Anomalies
      </Typography>
      <List>
        {mockAnomalies.map((anomaly) => (
          <React.Fragment key={anomaly.id}>
            <ListItem button onClick={() => handleToggle(anomaly.id)}>
              <ListItemText
                primary={anomaly.type}
                secondary={`Detected at: ${new Date(anomaly.timestamp).toLocaleString()}`}
              />
              <ListItemSecondaryAction>
                <IconButton edge="end" onClick={() => handleToggle(anomaly.id)}>
                  {expanded === anomaly.id ? <ExpandLess /> : <ExpandMore />}
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
            <Collapse in={expanded === anomaly.id} timeout="auto" unmountOnExit>
              <Box sx={{ pl: 4, pr: 2, pb: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  {anomaly.details}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Faces Detected: {anomaly.facesDetected.join(', ')}
                </Typography>
              </Box>
            </Collapse>
            <Divider />
          </React.Fragment>
        ))}
      </List>
    </Box>
  );
};

export default AnomaliesList;