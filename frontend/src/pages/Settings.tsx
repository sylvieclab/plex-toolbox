import { Container, Typography, Box } from '@mui/material';

const Settings = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" gutterBottom>
          Settings
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Configure Plex Toolbox settings and preferences
        </Typography>
        <Box sx={{ mt: 3 }}>
          <Typography variant="body2" color="text.secondary">
            Coming soon...
          </Typography>
        </Box>
      </Box>
    </Container>
  );
};

export default Settings;
