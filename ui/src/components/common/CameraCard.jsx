import { useState, useEffect, useRef } from 'react';
import {
  Card,
  CardContent,
  CardMedia,
  Typography,
  Box,
  IconButton,
  Chip,
  Menu,
  MenuItem,
  Collapse,
  LinearProgress,
} from '@mui/material';
import {
  Fullscreen,
  MoreVert,
  Warning,
  PeopleAlt,
  Timeline,
  Videocam,
  VideocamOff,
  TrendingUp,
} from '@mui/icons-material';

const CameraCard = ({ camera }) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const [showStats, setShowStats] = useState(false);
  const [streamStatus, setStreamStatus] = useState('active');
  const [loading, setLoading] = useState(false);
  const videoRef = useRef(null);

  useEffect(() => {
    if (camera.isSystemCamera && camera.stream && videoRef.current) {
      videoRef.current.srcObject = camera.stream;
    }
  }, [camera.isSystemCamera, camera.stream]);

  // Simulate stream status check
  useEffect(() => {
    const checkStream = () => {
      setLoading(true);
      setTimeout(() => {
        setStreamStatus(Math.random() > 0.2 ? 'active' : 'inactive');
        setLoading(false);
      }, 1000);
    };

    checkStream();
    const interval = setInterval(checkStream, 30000);

    return () => clearInterval(interval);
  }, []);

  const handleMenuClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const getAlertColor = (count) => {
    if (count > 5) return 'error';
    if (count > 2) return 'warning';
    return 'success';
  };

  const getDensityColor = (density) => {
    if (density > 0.7) return 'error';
    if (density > 0.4) return 'warning';
    return 'success';
  };

  const handleFullscreen = () => {
    if (videoRef.current) {
      if (videoRef.current.requestFullscreen) {
        videoRef.current.requestFullscreen();
      } else if (videoRef.current.mozRequestFullScreen) { /* Firefox */
        videoRef.current.mozRequestFullScreen();
      } else if (videoRef.current.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
        videoRef.current.webkitRequestFullscreen();
      } else if (videoRef.current.msRequestFullscreen) { /* IE/Edge */
        videoRef.current.msRequestFullscreen();
      }
    }
  };

  return (
    <Card sx={{ 
      position: 'relative',
      '&:hover': {
        boxShadow: 6,
        transform: 'translateY(-2px)',
        transition: 'all 0.3s ease-in-out'
      }
    }}>
      {loading && <LinearProgress />}
      
      <Box sx={{ position: 'relative', height: 200 }}>
        {camera.isSystemCamera ? (
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              filter: streamStatus === 'inactive' ? 'grayscale(100%)' : 'none',
            }}
          />
        ) : (
          <CardMedia
            component="img"
            height="200"
            image={camera.stream}
            alt={camera.name}
            sx={{
              filter: streamStatus === 'inactive' ? 'grayscale(100%)' : 'none',
            }}
          />
        )}
        
        {/* Stream Status Indicator */}
        <Box
          sx={{
            position: 'absolute',
            top: 8,
            left: 8,
            display: 'flex',
            alignItems: 'center',
            bgcolor: 'rgba(0, 0, 0, 0.6)',
            borderRadius: 1,
            px: 1,
            py: 0.5,
          }}
        >
          {streamStatus === 'active' ? (
            <Videocam sx={{ color: 'success.main', mr: 1 }} />
          ) : (
            <VideocamOff sx={{ color: 'error.main', mr: 1 }} />
          )}
          <Typography variant="caption" sx={{ color: 'white' }}>
            {streamStatus === 'active' ? 'Live' : 'Offline'}
          </Typography>
        </Box>

        {/* Metrics Chips */}
        <Box
          sx={{
            position: 'absolute',
            top: 8,
            right: 8,
            display: 'flex',
            gap: 1,
          }}
        >
          <Chip
            icon={<PeopleAlt />}
            label={`${camera.metrics.personCount}`}
            size="small"
            color={getDensityColor(camera.metrics.crowdDensity)}
            sx={{ bgcolor: 'rgba(255, 255, 255, 0.9)' }}
          />
          {camera.metrics.alerts > 0 && (
            <Chip
              icon={<Warning />}
              label={camera.metrics.alerts}
              size="small"
              color={getAlertColor(camera.metrics.alerts)}
              sx={{ bgcolor: 'rgba(255, 255, 255, 0.9)' }}
            />
          )}
        </Box>

        {/* Control Buttons */}
        <Box
          sx={{
            position: 'absolute',
            bottom: 8,
            right: 8,
            display: 'flex',
            gap: 1,
          }}
        >
          <IconButton
            onClick={handleFullscreen}
            sx={{ bgcolor: 'rgba(0, 0, 0, 0.6)', '&:hover': { bgcolor: 'rgba(0, 0, 0, 0.8)' } }}
          >
            <Fullscreen sx={{ color: 'white' }} />
          </IconButton>
          <IconButton
            onClick={handleMenuClick}
            sx={{ bgcolor: 'rgba(0, 0, 0, 0.6)', '&:hover': { bgcolor: 'rgba(0, 0, 0, 0.8)' } }}
          >
            <MoreVert sx={{ color: 'white' }} />
          </IconButton>
        </Box>
      </Box>

      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
          <Typography variant="h6" component="div">
            {camera.name}
          </Typography>
          <IconButton size="small" onClick={() => setShowStats(!showStats)}>
            <Timeline />
          </IconButton>
        </Box>
        
        <Typography variant="body2" color="text.secondary" gutterBottom>
          {camera.location}
        </Typography>

        <Collapse in={showStats}>
          <Box sx={{ mt: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2">Crowd Density:</Typography>
              <Typography variant="body2" color={getDensityColor(camera.metrics.crowdDensity)}>
                {(camera.metrics.crowdDensity * 100).toFixed(1)}%
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
              <Typography variant="body2">Trend:</Typography>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <TrendingUp color="success" sx={{ mr: 1 }} />
                <Typography variant="body2">+12%</Typography>
              </Box>
            </Box>
          </Box>
        </Collapse>
      </CardContent>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleMenuClose}>View Details</MenuItem>
        <MenuItem onClick={handleMenuClose}>Download Footage</MenuItem>
        <MenuItem onClick={handleMenuClose}>Configure Alerts</MenuItem>
        <MenuItem onClick={handleMenuClose}>View Analytics</MenuItem>
      </Menu>
    </Card>
  );
};

export default CameraCard;