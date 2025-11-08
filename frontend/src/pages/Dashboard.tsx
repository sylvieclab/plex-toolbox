import { 
  Container, 
  Typography, 
  Box, 
  Grid, 
  Paper,
  Button,
  CircularProgress,
  Alert,
  Chip,
  Stack,
  LinearProgress,
} from '@mui/material';
import {
  Movie as MovieIcon,
  Tv as TvIcon,
  Download as DownloadIcon,
  Search as SearchIcon,
  Speed as SpeedIcon,
  CheckCircle as CheckCircleIcon,
  CloudDownload as CloudDownloadIcon,
  VideoLibrary as VideoLibraryIcon,
} from '@mui/icons-material';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../services/api';

interface DashboardData {
  plex: {
    total_libraries: number;
    total_items: number;
    by_type: {
      movie: number;
      show: number;
      artist: number;
      photo: number;
    };
  };
  sabnzbd: {
    active_downloads: number;
    speed: string;
    queue_size: string;
    paused: boolean;
  } | null;
  sonarr: {
    total_series: number;
    missing_episodes: number;
  } | null;
  radarr: {
    total_movies: number;
    missing_movies: number;
  } | null;
  prowlarr: {
    total_indexers: number;
    enabled_indexers: number;
  } | null;
}

const Dashboard = () => {
  const navigate = useNavigate();
  
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load Plex stats
      const plexStats = await apiClient.getDashboardStats();

      // Initialize data object
      const dashboardData: DashboardData = {
        plex: plexStats,
        sabnzbd: null,
        sonarr: null,
        radarr: null,
        prowlarr: null,
      };

      // Try to load SABnzbd data
      try {
        const sabnzbdStatus = await apiClient.getSabnzbdStatus();
        const sabnzbdQueue = await apiClient.getSabnzbdQueue();
        dashboardData.sabnzbd = {
          active_downloads: sabnzbdQueue.queue?.slots?.length || 0,
          speed: sabnzbdStatus.speed || '0 B/s',
          queue_size: sabnzbdStatus.size_left || '0 B',
          paused: sabnzbdStatus.paused || false,
        };
      } catch (err) {
        console.log('SABnzbd not configured or unavailable');
      }

      // Try to load Sonarr data
      try {
        const sonarrSeries = await apiClient.getSonarrSeries();
        const sonarrMissing = await apiClient.getSonarrMissing(1, 1);
        dashboardData.sonarr = {
          total_series: sonarrSeries.length,
          missing_episodes: sonarrMissing.totalRecords || 0,
        };
      } catch (err) {
        console.log('Sonarr not configured or unavailable');
      }

      // Try to load Radarr data
      try {
        const radarrMovies = await apiClient.getRadarrMovies();
        const radarrMissing = await apiClient.getRadarrMissing();
        dashboardData.radarr = {
          total_movies: radarrMovies.length,
          missing_movies: radarrMissing.length,
        };
      } catch (err) {
        console.log('Radarr not configured or unavailable');
      }

      // Try to load Prowlarr data
      try {
        const prowlarrIndexers = await apiClient.getProwlarrIndexers();
        dashboardData.prowlarr = {
          total_indexers: prowlarrIndexers.length,
          enabled_indexers: prowlarrIndexers.filter((i: any) => i.enable).length,
        };
      } catch (err) {
        console.log('Prowlarr not configured or unavailable');
      }

      setData(dashboardData);
    } catch (err: any) {
      console.error('Error loading dashboard:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
    
    // Refresh every 30 seconds
    const interval = setInterval(loadDashboardData, 30000);
    return () => clearInterval(interval);
  }, []);

  if (loading && !data) {
    return (
      <Container maxWidth="xl">
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '60vh' }}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="xl">
        <Box sx={{ py: 4 }}>
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
          <Button variant="contained" onClick={loadDashboardData}>
            Retry
          </Button>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl">
      <Box sx={{ py: 4 }}>
        {/* Header */}
        <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Box>
            <Typography variant="h4" gutterBottom>
              Dashboard
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Overview of your media automation stack
            </Typography>
          </Box>
          <Button variant="outlined" onClick={loadDashboardData}>
            Refresh
          </Button>
        </Box>

        {/* Plex Stats */}
        <Typography variant="h5" sx={{ mb: 2 }}>
          <VideoLibraryIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
          Plex Media Server
        </Typography>
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <Typography variant="h3" color="primary">
                {data?.plex.total_libraries || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Libraries
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <Typography variant="h3" color="primary">
                {data?.plex.total_items.toLocaleString() || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total Items
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <MovieIcon sx={{ fontSize: 40, color: '#e50914', mb: 1 }} />
              <Typography variant="h4">
                {data?.plex.by_type.movie || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Movies
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <TvIcon sx={{ fontSize: 40, color: '#2196f3', mb: 1 }} />
              <Typography variant="h4">
                {data?.plex.by_type.show || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                TV Shows
              </Typography>
            </Paper>
          </Grid>
        </Grid>

        {/* SABnzbd Stats */}
        {data?.sabnzbd && (
          <>
            <Typography variant="h5" sx={{ mb: 2 }}>
              <DownloadIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
              Downloads (SABnzbd)
            </Typography>
            <Grid container spacing={3} sx={{ mb: 4 }}>
              <Grid item xs={12} md={8}>
                <Paper sx={{ p: 3 }}>
                  <Stack direction="row" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography variant="h6">Active Downloads</Typography>
                    <Chip 
                      label={data.sabnzbd.paused ? 'Paused' : 'Active'} 
                      color={data.sabnzbd.paused ? 'default' : 'success'}
                      size="small"
                    />
                  </Stack>
                  <Box sx={{ mb: 2 }}>
                    <Stack direction="row" justifyContent="space-between" mb={1}>
                      <Typography variant="body2" color="text.secondary">
                        {data.sabnzbd.active_downloads} item(s) in queue
                      </Typography>
                      <Typography variant="body2" fontWeight="bold">
                        <SpeedIcon sx={{ fontSize: 16, verticalAlign: 'middle' }} /> {data.sabnzbd.speed}
                      </Typography>
                    </Stack>
                    {data.sabnzbd.active_downloads > 0 && (
                      <LinearProgress variant="indeterminate" />
                    )}
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    Queue Size: {data.sabnzbd.queue_size}
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} md={4}>
                <Paper sx={{ p: 3, textAlign: 'center', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                  <CloudDownloadIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
                  <Typography variant="h3" color="primary">
                    {data.sabnzbd.active_downloads}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Active Downloads
                  </Typography>
                </Paper>
              </Grid>
            </Grid>
          </>
        )}

        {/* Sonarr & Radarr Stats */}
        <Grid container spacing={3} sx={{ mb: 4 }}>
          {data?.sonarr && (
            <Grid item xs={12} md={6}>
              <Typography variant="h5" sx={{ mb: 2 }}>
                <TvIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
                Sonarr (TV Shows)
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Paper sx={{ p: 3, textAlign: 'center' }}>
                    <CheckCircleIcon sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                    <Typography variant="h4">
                      {data.sonarr.total_series}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Total Series
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6}>
                  <Paper sx={{ p: 3, textAlign: 'center' }}>
                    <SearchIcon sx={{ fontSize: 40, color: 'warning.main', mb: 1 }} />
                    <Typography variant="h4" color="warning.main">
                      {data.sonarr.missing_episodes}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Missing Episodes
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </Grid>
          )}

          {data?.radarr && (
            <Grid item xs={12} md={6}>
              <Typography variant="h5" sx={{ mb: 2 }}>
                <MovieIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
                Radarr (Movies)
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Paper sx={{ p: 3, textAlign: 'center' }}>
                    <CheckCircleIcon sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                    <Typography variant="h4">
                      {data.radarr.total_movies}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Total Movies
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={6}>
                  <Paper sx={{ p: 3, textAlign: 'center' }}>
                    <SearchIcon sx={{ fontSize: 40, color: 'warning.main', mb: 1 }} />
                    <Typography variant="h4" color="warning.main">
                      {data.radarr.missing_movies}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Missing Movies
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </Grid>
          )}
        </Grid>

        {/* Prowlarr Stats */}
        {data?.prowlarr && (
          <>
            <Typography variant="h5" sx={{ mb: 2 }}>
              <SearchIcon sx={{ verticalAlign: 'middle', mr: 1 }} />
              Prowlarr (Indexers)
            </Typography>
            <Grid container spacing={3} sx={{ mb: 4 }}>
              <Grid item xs={12} sm={6}>
                <Paper sx={{ p: 3, textAlign: 'center' }}>
                  <CheckCircleIcon sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                  <Typography variant="h4">
                    {data.prowlarr.enabled_indexers}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Enabled Indexers
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Paper sx={{ p: 3, textAlign: 'center' }}>
                  <Typography variant="h4">
                    {data.prowlarr.total_indexers}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Total Indexers
                  </Typography>
                </Paper>
              </Grid>
            </Grid>
          </>
        )}

        {/* Missing Integrations Alert */}
        {(!data?.sabnzbd || !data?.sonarr || !data?.radarr || !data?.prowlarr) && (
          <Alert severity="info" sx={{ mb: 3 }}>
            <Typography variant="body2" gutterBottom>
              <strong>Configure More Integrations</strong>
            </Typography>
            <Typography variant="body2">
              Add integrations for {[
                !data?.sabnzbd && 'SABnzbd',
                !data?.sonarr && 'Sonarr',
                !data?.radarr && 'Radarr',
                !data?.prowlarr && 'Prowlarr',
              ].filter(Boolean).join(', ')} to see more stats on your dashboard.
            </Typography>
            <Button 
              size="small" 
              variant="outlined" 
              sx={{ mt: 1 }}
              onClick={() => navigate('/integrations')}
            >
              Go to Integrations
            </Button>
          </Alert>
        )}

        {/* Quick Actions */}
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Quick Actions
          </Typography>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="outlined"
                onClick={() => navigate('/libraries')}
                sx={{ py: 1.5 }}
              >
                View Libraries
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="outlined"
                onClick={() => navigate('/integrations')}
                sx={{ py: 1.5 }}
              >
                Manage Integrations
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="outlined"
                onClick={loadDashboardData}
                sx={{ py: 1.5 }}
              >
                Refresh Dashboard
              </Button>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Button
                fullWidth
                variant="outlined"
                onClick={() => navigate('/settings')}
                sx={{ py: 1.5 }}
              >
                Settings
              </Button>
            </Grid>
          </Grid>
        </Paper>
      </Box>
    </Container>
  );
};

export default Dashboard;
