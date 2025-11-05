import { useState, FormEvent } from 'react';
import {
  Container,
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Alert,
  CircularProgress,
} from '@mui/material';
import { apiClient } from '../services/api';
import { useAppStore } from '../store';
import { PlexServerConfig } from '../types';

const Setup = () => {
  const [config, setConfig] = useState<PlexServerConfig>({
    url: '',
    token: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const { setPlexConnected, setPlexServerInfo } = useAppStore();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      // Test connection
      const testResponse = await apiClient.connectToPlex(config);
      
      if (!testResponse.success) {
        throw new Error(testResponse.error || 'Failed to connect');
      }
      
      // Save configuration
      await apiClient.savePlexConfig(config);
      
      // Update store with server info
      if (testResponse.server_name) {
        setPlexServerInfo({
          name: testResponse.server_name,
          version: testResponse.version || '',
          platform: testResponse.platform || '',
          platform_version: '',
          machine_identifier: '',
        });
      }
      setPlexConnected(true);
      setSuccess(true);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to connect to Plex server');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Paper sx={{ p: 4, width: '100%' }}>
          <Typography variant="h4" gutterBottom align="center">
            Plex Toolbox Setup
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph align="center">
            Connect to your Plex Media Server to get started
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {success && (
            <Alert severity="success" sx={{ mb: 2 }}>
              Successfully connected to Plex server!
            </Alert>
          )}

          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Plex Server URL"
              placeholder="http://192.168.1.100:32400"
              value={config.url}
              onChange={(e) => setConfig({ ...config, url: e.target.value })}
              margin="normal"
              required
              helperText="Enter your Plex server URL (including port)"
            />

            <TextField
              fullWidth
              label="Plex Token"
              type="password"
              value={config.token}
              onChange={(e) => setConfig({ ...config, token: e.target.value })}
              margin="normal"
              required
              helperText="Your Plex authentication token"
            />

            <Box sx={{ mt: 3 }}>
              <Button
                type="submit"
                variant="contained"
                fullWidth
                size="large"
                disabled={loading}
              >
                {loading ? <CircularProgress size={24} /> : 'Connect to Plex'}
              </Button>
            </Box>
          </form>

          <Box sx={{ mt: 3 }}>
            <Typography variant="caption" color="text.secondary">
              Don't know how to find your Plex token?{' '}
              <a
                href="https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/"
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: '#e5a00d' }}
              >
                Learn how
              </a>
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default Setup;
