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
  Collapse,
  ThemeProvider,
  createTheme 
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

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    background: {
      default: '#121212',
      paper: '#1E1E1E',
    },
    text: {
      primary: '#FFFFFF',
      secondary: 'rgba(255, 255, 255, 0.7)',
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '12px',
          border: '1px solid rgba(255, 255, 255, 0.12)',
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          fontWeight: 500,
          letterSpacing: 0.5,
        },
      },
    },
  },
});

const getSeverityIcon = (severity) => {
  switch (severity) {
    case 'high':
      return <Error sx={{ color: darkTheme.palette.error.main }} />;
    case 'medium':
      return <Warning sx={{ color: darkTheme.palette.warning.main }} />;
    default:
      return <Info sx={{ color: darkTheme.palette.info.main }} />;
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
    <ThemeProvider theme={darkTheme}>
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
            Recent Alerts
          </Typography>
          <List disablePadding>
            {alerts.map((alert) => (
              <React.Fragment key={alert.id}>
                <ListItem 
                  divider 
                  sx={{
                    backgroundColor: darkTheme.palette.background.paper,
                    '&:hover': {
                      backgroundColor: 'rgba(255, 255, 255, 0.05)',
                    },
                    transition: 'background-color 0.2s ease',
                  }}
                  secondaryAction={
                    <IconButton 
                      onClick={() => handleExpand(alert.id)}
                      sx={{ color: darkTheme.palette.text.secondary }}
                    >
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
                        <Typography variant="subtitle1" sx={{ fontWeight: 500 }}>
                          {alert.type}
                        </Typography>
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
                    secondary={
                      <Box sx={{ display: 'flex', gap: 2, mt: 0.5 }}>
                        <Typography variant="caption" sx={{ opacity: 0.8 }}>
                          {new Date(alert.timestamp).toLocaleString()}
                        </Typography>
                        <Typography variant="caption" sx={{ opacity: 0.8 }}>
                          {alert.location}
                        </Typography>
                      </Box>
                    }
                  />
                </ListItem>
                <Collapse in={expandedId === alert.id}>
                  <Box sx={{ 
                    p: 2, 
                    backgroundColor: 'rgba(255, 255, 255, 0.08)', 
                    borderBottom: `1px solid ${darkTheme.palette.divider}` 
                  }}>
                    <Typography variant="body2" paragraph sx={{ opacity: 0.9 }}>
                      {alert.details}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Person fontSize="small" sx={{ color: darkTheme.palette.text.secondary }} />
                      <Typography variant="body2" sx={{ opacity: 0.9 }}>
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
    </ThemeProvider>
  );
};

export default AlertsPanel;