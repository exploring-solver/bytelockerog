import { 
    AppBar, 
    Toolbar, 
    IconButton, 
    Typography, 
    Badge,
    Box 
  } from '@mui/material';
  import {
    Menu,
    Notifications,
    DarkMode,
    LightMode,
  } from '@mui/icons-material';
  
  const Header = ({ onMenuClick, onThemeToggle, darkMode }) => {
    return (
      <AppBar position="fixed">
        <Toolbar>
          <IconButton
            color="inherit"
            edge="start"
            onClick={onMenuClick}
            sx={{ mr: 2 }}
          >
            <Menu />
          </IconButton>
          
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            AI CCTV Monitoring System - Bytelocker
          </Typography>
  
          <Box sx={{ display: 'flex' }}>
            <IconButton color="inherit" onClick={onThemeToggle}>
              {darkMode ? <LightMode /> : <DarkMode />}
            </IconButton>
            
            <IconButton color="inherit">
              <Badge badgeContent={4} color="error">
                <Notifications />
              </Badge>
            </IconButton>
          </Box>
        </Toolbar>
      </AppBar>
    );
  };
  
  export default Header;