import { Container, Typography, Box, Grid, Paper } from '@mui/material';
import { useAppStore } from '../store';

const Dashboard = () => {
  const { plexServerInfo } = useAppStore();

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Welcome to Plex Toolbox - Your advanced Plex management tool
        </Typography>

        {plexServerInfo && (
          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Server Information
                </Typography>
                <Typography variant="body2">
                  <strong>Name:</strong> {plexServerInfo.name}
                </Typography>
                <Typography variant="body2">
                  <strong>Version:</strong> {plexServerInfo.version}
                </Typography>
                <Typography variant="body2">
                  <strong>Platform:</strong> {plexServerInfo.platform}
                </Typography>
              </Paper>
            </Grid>

            <Grid item xs={12} md={6}>
              <Paper sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  Quick Stats
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Coming soon...
                </Typography>
              </Paper>
            </Grid>
          </Grid>
        )}
      </Box>
    </Container>
  );
};

export default Dashboard;
