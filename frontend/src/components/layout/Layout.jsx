import { useState } from 'react';
import { Outlet } from 'react-router-dom';
import { Box, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import Sidebar from './Sidebar';
import Header from './Header';
import Footer from './Footer';

const Layout = () => {
  const [darkMode, setDarkMode] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const theme = createTheme({
    palette: {
      mode: darkMode ? 'dark' : 'light',
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex' }}>
        <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
        <Box sx={{ flexGrow: 1 }}>
          <Header 
            onMenuClick={() => setSidebarOpen(true)}
            onThemeToggle={() => setDarkMode(!darkMode)}
            darkMode={darkMode}
          />
          <Box component="main" sx={{ p: 3, mt: 8 }}>
            <Outlet />
          </Box>
          <Footer />
        </Box>
      </Box>
    </ThemeProvider>
  );
};

export default Layout;