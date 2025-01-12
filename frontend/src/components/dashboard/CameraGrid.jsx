import { useState, useEffect, useRef } from 'react';
import { Grid, Box, Typography, Modal, Button, TextField, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import CameraCard from '../common/CameraCard';

// Mock data for system cameras
const mockSystemCameras = [
  { id: 'webcam-1', label: 'Built-in Webcam' },
  { id: 'webcam-2', label: 'USB Camera' },
  { id: 'webcam-3', label: 'IP Camera 1' },
  { id: 'webcam-4', label: 'Conference Room Camera' }
];

const initialCameras = [
  {
    id: 1,
    name: 'System Camera',
    location: 'Local Device',
    stream: null,
    isSystemCamera: true,
    metrics: {
      crowdDensity: 0.45,
      personCount: 12,
      alerts: 2
    }
  },
  {
    id: 2,
    name: 'Main Entrance',
    location: 'Building A',
    stream: '/mock-streams/camera1.mp4',
    metrics: {
      crowdDensity: 0.45,
      personCount: 12,
      alerts: 2
    }
  },
  // Additional mock cameras...
];

const CameraGrid = ({ viewMode }) => {
  const [cameras, setCameras] = useState(initialCameras);
  const [selectedCamera, setSelectedCamera] = useState(null);
  const [openAddCameraModal, setOpenAddCameraModal] = useState(false);
  const [newCamera, setNewCamera] = useState({
    name: '',
    location: '',
    stream: '',
    systemCameraId: ''
  });
  const [systemCameras, setSystemCameras] = useState([]);
  const [loading, setLoading] = useState(true);
  const videoRef = useRef(null);
  const streamRef = useRef(null);


  useEffect(() => {
    // Simulate fetching system cameras
    const fetchSystemCameras = async () => {
      try {
        // In a real implementation, this would be an API call to get available system cameras
        await new Promise(resolve => setTimeout(resolve, 1000));
        setSystemCameras(mockSystemCameras);
      } catch (error) {
        console.error('Error fetching system cameras:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSystemCameras();
  }, []);

  useEffect(() => {
    // Initialize system camera
    const initializeCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        streamRef.current = stream;

        // Update the first camera with the live stream
        setCameras(prevCameras => prevCameras.map((camera, index) => {
          if (index === 0 && camera.isSystemCamera) {
            return {
              ...camera,
              stream: stream
            };
          }
          return camera;
        }));
      } catch (error) {
        console.error('Error accessing camera:', error);
      }
    };

    initializeCamera();

    // Cleanup function to stop the stream
    return () => {
      if (streamRef.current) {
        const tracks = streamRef.current.getTracks();
        tracks.forEach(track => track.stop());
      }
    };
  }, []);

  // const handleAddCamera = () => {
  //   setCameras([...cameras, { 
  //     ...newCamera, 
  //     id: cameras.length + 1, 
  //     metrics: { crowdDensity: 0, personCount: 0, alerts: 0 } 
  //   }]);
  //   setNewCamera({ name: '', location: '', stream: '' });
  //   setOpenAddCameraModal(false);
  // };
  const handleAddCamera = () => {
    const selectedSystemCamera = systemCameras.find(cam => cam.id === newCamera.systemCameraId);
    const newCameraEntry = {
      ...newCamera,
      id: cameras.length + 1,
      metrics: { crowdDensity: 0, personCount: 0, alerts: 0 },
      // Keep mock stream if no system camera is selected, otherwise use system camera
      stream: newCamera.systemCameraId ? `system-camera://${newCamera.systemCameraId}` : newCamera.stream
    };

    setCameras([...cameras, newCameraEntry]);
    setNewCamera({ name: '', location: '', stream: '', systemCameraId: '' });
    setOpenAddCameraModal(false);
  };

  const handleSystemCameraChange = (cameraId) => {
    setNewCamera(prev => ({
      ...prev,
      systemCameraId: cameraId,
      // Clear custom stream URL if system camera is selected
      stream: cameraId ? '' : prev.stream
    }));
  };

  return (
    <Box>
      <Typography variant="h6" sx={{ mb: 2 }}>
        Live Camera Feeds
      </Typography>

      <Button variant="contained" onClick={() => setOpenAddCameraModal(true)}>
        Add Camera
      </Button>

      <Grid container spacing={2} sx={{ mt: 2 }}>
        {cameras.map((camera) => (
          <Grid
            item
            xs={12}
            md={viewMode === 'grid' ? 6 : 12}
            key={camera.id}
          >
            <CameraCard
              camera={camera}
              onFullscreen={() => setSelectedCamera(camera)}
            />
          </Grid>
        ))}
      </Grid>

      {/* Modal for Fullscreen Camera View */}
      <Modal
        open={Boolean(selectedCamera)}
        onClose={() => setSelectedCamera(null)}
        sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}
      >
        <Box sx={{ width: '90vw', height: '90vh', bgcolor: 'background.paper', borderRadius: 1, p: 2 }}>
          {selectedCamera && (
            <>
              <Typography variant="h6" sx={{ mb: 2 }}>
                {selectedCamera.name} - {selectedCamera.location}
              </Typography>
              {selectedCamera.isSystemCamera ? (
                <video
                  ref={videoRef}
                  style={{ width: '100%', height: 'calc(100% - 50px)' }}
                  autoPlay
                  playsInline
                  muted
                />
              ) : (
                <video
                  src={selectedCamera.stream}
                  style={{ width: '100%', height: 'calc(100% - 50px)' }}
                  autoPlay
                  controls
                />
              )}
            </>
          )}
        </Box>
      </Modal>

      {/* Modal for Adding New Camera */}
      <Modal
        open={openAddCameraModal}
        onClose={() => setOpenAddCameraModal(false)}
        sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}
      >
        <Box sx={{ width: 400, bgcolor: 'background.paper', borderRadius: 1, p: 2 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>
            Add New Camera
          </Typography>

          <FormControl fullWidth sx={{ mb: 2 }}>
            <InputLabel>System Camera</InputLabel>
            <Select
              value={newCamera.systemCameraId}
              onChange={(e) => handleSystemCameraChange(e.target.value)}
              label="System Camera"
            >
              <MenuItem value="">
                <em>None (Use Custom Stream)</em>
              </MenuItem>
              {systemCameras.map((cam) => (
                <MenuItem key={cam.id} value={cam.id}>
                  {cam.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <TextField
            label="Camera Name"
            fullWidth
            value={newCamera.name}
            onChange={(e) => setNewCamera({ ...newCamera, name: e.target.value })}
            sx={{ mb: 2 }}
          />
          <TextField
            label="Location"
            fullWidth
            value={newCamera.location}
            onChange={(e) => setNewCamera({ ...newCamera, location: e.target.value })}
            sx={{ mb: 2 }}
          />
          {!newCamera.systemCameraId && (
            <TextField
              label="Custom Stream URL"
              fullWidth
              value={newCamera.stream}
              onChange={(e) => setNewCamera({ ...newCamera, stream: e.target.value })}
              sx={{ mb: 2 }}
            />
          )}
          <Button
            variant="contained"
            onClick={handleAddCamera}
            fullWidth
            disabled={!newCamera.name || (!newCamera.systemCameraId && !newCamera.stream)}
          >
            Add Camera
          </Button>
        </Box>
      </Modal>
    </Box>
  );
};

export default CameraGrid;