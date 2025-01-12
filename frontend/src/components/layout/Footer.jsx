// src/components/layout/Footer.jsx
import { Box, Typography } from '@mui/material';
import FavoriteIcon from '@mui/icons-material/Favorite';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 2,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) => theme.palette.mode === 'light' ? theme.palette.grey[200] : theme.palette.grey[800],
        position: 'fixed',
        bottom: 0,
        width: '100%',
        textAlign: 'center',
        borderTop: '1px solid',
        borderColor: 'divider',
      }}
    >
      <Typography variant="body2" color="text.secondary" align="center" className='!font-bold'>
        Made with{' '}
        <FavoriteIcon
          sx={{
            color: 'error.main',
            fontSize: 16,
            verticalAlign: 'middle',
            animation: 'pulse 1.5s infinite',
            '@keyframes pulse': {
              '0%': { transform: 'scale(1)' },
              '50%': { transform: 'scale(1.2)' },
              '100%': { transform: 'scale(1)' },
            },
          }}
        />{' '}
        by team Sangathan for CodeFiesta 6.0 - ByteLocker
      </Typography>
    </Box>
  );
};

export default Footer;