import { Drawer, List, ListItem, ListItemIcon, ListItemText, IconButton } from '@mui/material';
import {
  Dashboard,
  Security,
  Analytics,
  Settings,
  ChevronLeft,
  PanoramaFishEyeTwoTone,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const Sidebar = ({ open, onClose }) => {
  const navigate = useNavigate();

  const menuItems = [
    { text: 'Dashboard', icon: <Dashboard />, path: '/' },
    { text: 'Security', icon: <Security />, path: '/security' },
    { text: 'Vision Language Model', icon: <PanoramaFishEyeTwoTone />, path: '/vlm' },
    { text: 'Analytics', icon: <Analytics />, path: '/analytics' },
    { text: 'Settings', icon: <Settings />, path: '/settings' },
  ];

  return (
    <Drawer
      variant="persistent"
      anchor="left"
      open={open}
      sx={{
        width: 240,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: 240,
          boxSizing: 'border-box',
        },
      }}
    >
      <IconButton onClick={onClose}>
        <ChevronLeft />
      </IconButton>
      <List>
        {menuItems.map((item) => (
          <ListItem 
            button 
            key={item.text} 
            onClick={() => navigate(item.path)}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar;