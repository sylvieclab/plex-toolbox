import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Button,
  Alert,
  CircularProgress,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { apiClient } from '../services/api';
import IntegrationCard from '../components/integrations/IntegrationCard';
import IntegrationDialog from '../components/integrations/IntegrationDialog';
import { IntegrationConfig, IntegrationServiceType } from '../types';

const Integrations = () => {
  const [integrations, setIntegrations] = useState<IntegrationConfig[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingIntegration, setEditingIntegration] = useState<IntegrationConfig | null>(null);

  const loadIntegrations = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getIntegrations();
      setIntegrations(data);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load integrations');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadIntegrations();
  }, []);

  const handleAdd = () => {
    setEditingIntegration(null);
    setDialogOpen(true);
  };

  const handleEdit = async (integration: IntegrationConfig) => {
    // Fetch full integration details (with complete API key)
    try {
      const fullIntegration = await apiClient.getIntegration(integration.id!);
      setEditingIntegration(fullIntegration);
      setDialogOpen(true);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load integration details');
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this integration?')) {
      return;
    }

    try {
      await apiClient.deleteIntegration(id);
      await loadIntegrations();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete integration');
    }
  };

  const handleToggleEnabled = async (integration: IntegrationConfig) => {
    try {
      await apiClient.updateIntegration(integration.id!, {
        enabled: !integration.enabled,
      });
      await loadIntegrations();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update integration');
    }
  };

  const handleDialogClose = () => {
    setDialogOpen(false);
    setEditingIntegration(null);
  };

  const handleDialogSave = async () => {
    await loadIntegrations();
    handleDialogClose();
  };

  const getIntegrationsByType = (serviceType: IntegrationServiceType) => {
    return integrations.filter((i) => i.service_type === serviceType);
  };

  const serviceTypes: Array<{ type: IntegrationServiceType; title: string; description: string }> = [
    {
      type: 'sabnzbd',
      title: 'SABnzbd',
      description: 'Download client for Usenet',
    },
    {
      type: 'sonarr',
      title: 'Sonarr',
      description: 'TV show management and automation',
    },
    {
      type: 'radarr',
      title: 'Radarr',
      description: 'Movie management and automation',
    },
    {
      type: 'prowlarr',
      title: 'Prowlarr',
      description: 'Indexer manager for *arr apps',
    },
  ];

  if (loading) {
    return (
      <Container>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Typography variant="h4" component="h1">
            Integrations
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={handleAdd}
          >
            Add Integration
          </Button>
        </Box>

        <Typography variant="body1" color="text.secondary" paragraph>
          Connect your media automation tools to Plex Toolbox. Manage downloads, monitor missing
          content, and automate your media library.
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
            {error}
          </Alert>
        )}
      </Box>

      <Grid container spacing={3}>
        {serviceTypes.map(({ type, title, description }) => {
          const serviceIntegrations = getIntegrationsByType(type);

          return (
            <Grid item xs={12} md={6} key={type}>
              <Paper sx={{ p: 3 }}>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                  <Box>
                    <Typography variant="h6">{title}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {description}
                    </Typography>
                  </Box>
                </Box>

                {serviceIntegrations.length === 0 ? (
                  <Box
                    sx={{
                      p: 3,
                      textAlign: 'center',
                      borderRadius: 1,
                      border: '1px solid',
                      borderColor: 'divider',
                    }}
                  >
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      No {title} integration configured
                    </Typography>
                    <Button
                      size="small"
                      variant="outlined"
                      onClick={() => {
                        setEditingIntegration({
                          service_type: type,
                          name: `Main ${title}`,
                          url: '',
                          api_key: '',
                          enabled: true,
                        });
                        setDialogOpen(true);
                      }}
                    >
                      Add {title}
                    </Button>
                  </Box>
                ) : (
                  <Box>
                    {serviceIntegrations.map((integration) => (
                      <IntegrationCard
                        key={integration.id}
                        integration={integration}
                        onEdit={() => handleEdit(integration)}
                        onDelete={() => handleDelete(integration.id!)}
                        onToggleEnabled={() => handleToggleEnabled(integration)}
                      />
                    ))}
                  </Box>
                )}
              </Paper>
            </Grid>
          );
        })}
      </Grid>

      <IntegrationDialog
        open={dialogOpen}
        integration={editingIntegration}
        onClose={handleDialogClose}
        onSave={handleDialogSave}
      />
    </Container>
  );
};

export default Integrations;
