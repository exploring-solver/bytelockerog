// src/pages/Settings.jsx
import { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Switch,
  FormGroup,
  FormControlLabel,
  TextField,
  Button,
  Grid,
} from '@mui/material';

const Settings = () => {
  const [settings, setSettings] = useState({
    enableNotifications: true,
    enableDarkMode: false,
    alertThreshold: 0.75,
    retentionDays: 30,
  });

  const handleChange = (event) => {
    const { name, value, checked } = event.target;
    setSettings(prev => ({
      ...prev,
      [name]: event.target.type === 'checkbox' ? checked : value
    }));
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3 }}>
        System Settings
      </Typography>
      
      <Paper sx={{ p: 3 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <FormGroup>
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.enableNotifications}
                    onChange={handleChange}
                    name="enableNotifications"
                  />
                }
                label="Enable Notifications"
              />
              <FormControlLabel
                control={
                  <Switch
                    checked={settings.enableDarkMode}
                    onChange={handleChange}
                    name="enableDarkMode"
                  />
                }
                label="Dark Mode"
              />
            </FormGroup>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Alert Threshold"
              type="number"
              name="alertThreshold"
              value={settings.alertThreshold}
              onChange={handleChange}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Data Retention (days)"
              type="number"
              name="retentionDays"
              value={settings.retentionDays}
              onChange={handleChange}
            />
          </Grid>
          
          <Grid item xs={12}>
            <Button variant="contained" color="primary">
              Save Settings
            </Button>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default Settings;