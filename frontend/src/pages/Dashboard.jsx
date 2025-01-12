import { useState, useEffect } from 'react';
import {
    Box,
    Grid,
    Paper,
    Typography,
    ToggleButtonGroup,
    ToggleButton
} from '@mui/material';
import { ViewModule, ViewList } from '@mui/icons-material';
import CameraGrid from '../components/dashboard/CameraGrid';
import MetricsPanel from '../components/dashboard/MetricsPanel';
import AlertsPanel from '../components/dashboard/AlertsPanel';
import { generateRandomMetrics } from '../utils/mockDataGenerator';

const Dashboard = () => {
    const [viewMode, setViewMode] = useState('grid');
    const [metrics, setMetrics] = useState({
        totalPeople: 0,
        crowdDensity: 0,
        alerts: [],
        violations: []
    });


    // Update metrics periodically
    useEffect(() => {
        const interval = setInterval(() => {
            setMetrics(generateRandomMetrics());
        }, 5000); // Update every 5 seconds

        return () => clearInterval(interval);
    }, []);
    useEffect(() => {
        // WebSocket connection for real-time updates
        const ws = new WebSocket('ws://your-backend-url/ws/metrics');

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            setMetrics(data);
        };

        return () => ws.close();
    }, []);

    return (
        <Box>
            <Box sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                mb: 3
            }}>
                <Typography variant="h4">CCTV Monitoring Dashboard</Typography>
                <ToggleButtonGroup
                    value={viewMode}
                    exclusive
                    onChange={(_, value) => value && setViewMode(value)}
                >
                    <ToggleButton value="grid">
                        <ViewModule />
                    </ToggleButton>
                    <ToggleButton value="list">
                        <ViewList />
                    </ToggleButton>
                </ToggleButtonGroup>
            </Box>

            <Grid container spacing={3}>
                <Grid item xs={12} lg={8}>
                    <Paper
                        elevation={3}
                        sx={{
                            p: 2,
                            height: 'calc(100vh - 180px)',
                            overflow: 'auto'
                        }}
                    >
                        <CameraGrid viewMode={viewMode} />
                    </Paper>
                </Grid>

                <Grid item xs={12} lg={4}>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <MetricsPanel metrics={metrics} />
                        </Grid>
                        <Grid item xs={12}>
                            <AlertsPanel alerts={metrics.alerts} />
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </Box>
    );
};

export default Dashboard;