import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
  Chip,
  LinearProgress,
  Paper,
  Stack,
  IconButton,
  Tooltip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Divider
} from '@mui/material';
import {
  Movie as MovieIcon,
  Tv as TvIcon,
  CloudDownload as DownloadIcon,
  Search as SearchIcon,
  Refresh as RefreshIcon,
  Storage as StorageIcon,
  Speed as SpeedIcon,
  CheckCircle as CheckCircleIcon,
  HourglassEmpty as HourglassIcon,
  TrendingUp as TrendingUpIcon,
  CalendarToday as CalendarIcon,
  AccessTime as TimeIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import axios from 'axios';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  subtitle?: string;
  color?: 'primary' | 'secondary' | 'success' | 'error' | 'warning' | 'info';
  progress?: number;
  infoTooltip?: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, subtitle, color = 'primary', progress, infoTooltip }) => (
  <Card sx={{ height: '100%', bgcolor: 'background.paper' }}>
    <CardContent sx={{ p: 1.5, '&:last-child': { pb: 1.5 } }}>
      <Stack spacing={0.5}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
            <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600, textTransform: 'uppercase', fontSize: '0.7rem' }}>
              {title}
            </Typography>
            {infoTooltip && (
              <Tooltip 
                title={infoTooltip} 
                arrow 
                placement="top"
                sx={{ cursor: 'help' }}
              >
                <InfoIcon sx={{ fontSize: 14, color: 'text.secondary', opacity: 0.6 }} />
              </Tooltip>
            )}
          </Box>
          <Box sx={{ color: `${color}.main`, fontSize: 16 }}>{icon}</Box>
        </Box>
        <Typography variant="h6" sx={{ fontWeight: 'bold', lineHeight: 1.2 }}>
          {value}
        </Typography>
        {subtitle && (
          <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.7rem' }}>
            {subtitle}
          </Typography>
        )}
        {progress !== undefined && (
          <LinearProgress 
            variant="determinate" 
            value={progress} 
            sx={{ 
              height: 3, 
              borderRadius: 1,
              mt: 0.5,
              backgroundColor: 'rgba(255,255,255,0.1)'
            }} 
          />
        )}
      </Stack>
    </CardContent>
  </Card>
);

const Statistics: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statistics, setStatistics] = useState<any>(null);
  const [refreshing, setRefreshing] = useState(false);

  const fetchStatistics = async (showRefreshing = false) => {
    try {
      if (showRefreshing) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }
      setError(null);

      const response = await axios.get('/api/statistics/overview');
      console.log('Statistics response:', response.data);
      setStatistics(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load statistics');
      console.error('Failed to fetch statistics:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchStatistics();
    
    // Auto-refresh every 30 seconds
    const interval = setInterval(() => {
      fetchStatistics(true);
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  const formatBytes = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  };

  const formatTimeRange = (range: any): string => {
    if (!range) return '';
    if (range.label === 'All Time') return range.label;
    return range.label;
  };

  if (loading && !statistics) {
    return (
      <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  // Check if any servers have article stats
  const hasArticleStats = statistics?.sabnzbd?.servers && 
    Object.values(statistics.sabnzbd.servers).some((server: any) => server.has_article_stats);

  // Tooltip content
  const rssQueriesTooltip = "RSS Queries are automated background checks. Your *arr apps regularly sync with indexers' RSS feeds (like a newsletter) to automatically monitor for new releases and upgrades to your monitored content. This uses minimal resources for both you and the indexer.";
  
  const searchQueriesTooltip = "Search Queries are manual searches that scan the indexer's full database. These happen when you manually click 'Search' for a specific movie/episode, when adding new content, or when requesting content through systems like Requestrr or Overseerr. Search queries use more resources, so they should be used sparingly to avoid overloading indexers.";

  return (
    <Container maxWidth="xl" sx={{ mt: 2, mb: 2 }}>
      {/* Compact Header with Time Range Info */}
      <Box sx={{ mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <Box>
          <Typography variant="h5" sx={{ fontWeight: 'bold', mb: 0.5 }}>
            Statistics Dashboard
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
              <TimeIcon sx={{ fontSize: 14, color: 'text.secondary' }} />
              <Typography variant="caption" color="text.secondary">
                Updated: {statistics?.timestamp ? new Date(statistics.timestamp).toLocaleTimeString() : ''}
              </Typography>
            </Box>
            {statistics?.time_ranges && (
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Chip label={formatTimeRange(statistics.time_ranges.today)} size="small" variant="outlined" />
                <Chip label={formatTimeRange(statistics.time_ranges.week)} size="small" variant="outlined" />
                <Chip label={formatTimeRange(statistics.time_ranges.month)} size="small" variant="outlined" />
                <Chip label="All Time" size="small" variant="outlined" />
              </Box>
            )}
          </Box>
        </Box>
        <Tooltip title="Refresh Statistics">
          <IconButton 
            onClick={() => fetchStatistics(true)} 
            disabled={refreshing}
            size="small"
          >
            <RefreshIcon sx={{ animation: refreshing ? 'spin 1s linear infinite' : 'none' }} />
          </IconButton>
        </Tooltip>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* Radarr Statistics */}
      {statistics?.radarr?.enabled && !statistics.radarr.error && (
        <Paper sx={{ p: 1.5, mb: 1.5 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <MovieIcon sx={{ fontSize: 20, mr: 0.75, color: 'primary.main' }} />
            <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
              Radarr
            </Typography>
          </Box>
          <Grid container spacing={1}>
            <Grid item xs={6} sm={3} md={2}>
              <StatCard
                title="Total"
                value={statistics.radarr.movies?.total || 0}
                icon={<MovieIcon fontSize="small" />}
                subtitle={`${statistics.radarr.movies?.monitored || 0} monitored`}
                color="primary"
              />
            </Grid>
            <Grid item xs={6} sm={3} md={2}>
              <StatCard
                title="Downloaded"
                value={statistics.radarr.movies?.downloaded || 0}
                icon={<CheckCircleIcon fontSize="small" />}
                subtitle={`${statistics.radarr.movies?.download_percentage || 0}%`}
                color="success"
                progress={statistics.radarr.movies?.download_percentage || 0}
              />
            </Grid>
            <Grid item xs={6} sm={3} md={2}>
              <StatCard
                title="Missing"
                value={statistics.radarr.movies?.missing || 0}
                icon={<HourglassIcon fontSize="small" />}
                color="warning"
              />
            </Grid>
            <Grid item xs={6} sm={3} md={2}>
              <StatCard
                title="Storage"
                value={`${statistics.radarr.storage?.total_size_gb || 0} GB`}
                icon={<StorageIcon fontSize="small" />}
                subtitle={`${statistics.radarr.storage?.disk_used_percentage || 0}% disk`}
                color="info"
              />
            </Grid>
            <Grid item xs={6} sm={3} md={2}>
              <StatCard
                title="Queue"
                value={statistics.radarr.queue?.total_items || 0}
                icon={<DownloadIcon fontSize="small" />}
                subtitle={`${statistics.radarr.queue?.downloading || 0} active`}
                color="secondary"
              />
            </Grid>
          </Grid>
        </Paper>
      )}

      {/* Sonarr Statistics */}
      {statistics?.sonarr?.enabled && !statistics.sonarr.error && (
        <Paper sx={{ p: 1.5, mb: 1.5 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <TvIcon sx={{ fontSize: 20, mr: 0.75, color: 'secondary.main' }} />
            <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
              Sonarr
            </Typography>
          </Box>
          <Grid container spacing={1}>
            <Grid item xs={6} sm={3} md={2}>
              <StatCard
                title="Series"
                value={statistics.sonarr.series?.total || 0}
                icon={<TvIcon fontSize="small" />}
                subtitle={`${statistics.sonarr.series?.continuing || 0} continuing`}
                color="secondary"
              />
            </Grid>
            <Grid item xs={6} sm={3} md={2}>
              <StatCard
                title="Episodes"
                value={statistics.sonarr.episodes?.total || 0}
                icon={<MovieIcon fontSize="small" />}
                subtitle={`${statistics.sonarr.episodes?.downloaded || 0} downloaded`}
                color="primary"
              />
            </Grid>
            <Grid item xs={6} sm={3} md={2}>
              <StatCard
                title="Progress"
                value={`${statistics.sonarr.episodes?.download_percentage || 0}%`}
                icon={<CheckCircleIcon fontSize="small" />}
                subtitle={`${statistics.sonarr.episodes?.missing || 0} missing`}
                color="success"
                progress={statistics.sonarr.episodes?.download_percentage || 0}
              />
            </Grid>
            <Grid item xs={6} sm={3} md={2}>
              <StatCard
                title="Storage"
                value={`${statistics.sonarr.storage?.total_size_gb || 0} GB`}
                icon={<StorageIcon fontSize="small" />}
                subtitle={`${statistics.sonarr.storage?.disk_used_percentage || 0}% disk`}
                color="info"
              />
            </Grid>
            <Grid item xs={6} sm={3} md={2}>
              <StatCard
                title="Queue"
                value={statistics.sonarr.queue?.total_items || 0}
                icon={<DownloadIcon fontSize="small" />}
                subtitle={`${statistics.sonarr.queue?.downloading || 0} active`}
                color="secondary"
              />
            </Grid>
          </Grid>
        </Paper>
      )}

      {/* SABnzbd Statistics */}
      {statistics?.sabnzbd?.enabled && !statistics.sabnzbd.error && (
        <Paper sx={{ p: 1.5, mb: 1.5 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <DownloadIcon sx={{ fontSize: 20, mr: 0.75, color: 'success.main' }} />
            <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
              SABnzbd
            </Typography>
          </Box>
          
          {/* Queue & Speed Stats */}
          <Grid container spacing={1} sx={{ mb: 1.5 }}>
            <Grid item xs={6} sm={3} md={1.5}>
              <StatCard
                title="Speed"
                value={`${statistics.sabnzbd.queue?.speed_mbps || 0} MB/s`}
                icon={<SpeedIcon fontSize="small" />}
                subtitle={statistics.sabnzbd.queue?.paused ? 'Paused' : 'Active'}
                color={statistics.sabnzbd.queue?.paused ? 'warning' : 'success'}
              />
            </Grid>
            <Grid item xs={6} sm={3} md={1.5}>
              <StatCard
                title="Active"
                value={statistics.sabnzbd.queue?.active_downloads || 0}
                icon={<DownloadIcon fontSize="small" />}
                subtitle={`${statistics.sabnzbd.queue?.size_left_mb || 0} MB left`}
                color="primary"
              />
            </Grid>
            <Grid item xs={6} sm={3} md={1.5}>
              <StatCard
                title="Today"
                value={`${statistics.sabnzbd.statistics?.day_gb || 0} GB`}
                icon={<CalendarIcon fontSize="small" />}
                color="info"
              />
            </Grid>
            <Grid item xs={6} sm={3} md={1.5}>
              <StatCard
                title="Week"
                value={`${statistics.sabnzbd.statistics?.week_gb || 0} GB`}
                icon={<TrendingUpIcon fontSize="small" />}
                color="info"
              />
            </Grid>
            <Grid item xs={6} sm={3} md={1.5}>
              <StatCard
                title="Month"
                value={`${statistics.sabnzbd.statistics?.month_gb || 0} GB`}
                icon={<TrendingUpIcon fontSize="small" />}
                color="info"
              />
            </Grid>
            <Grid item xs={6} sm={3} md={1.5}>
              <StatCard
                title="Total"
                value={`${statistics.sabnzbd.statistics?.total_gb || 0} GB`}
                icon={<CheckCircleIcon fontSize="small" />}
                color="success"
              />
            </Grid>
          </Grid>

          {/* Server Statistics Table */}
          {statistics.sabnzbd.servers && Object.keys(statistics.sabnzbd.servers).length > 0 ? (
            <>
              <Divider sx={{ my: 1 }} />
              <Typography variant="caption" sx={{ mb: 0.5, display: 'block', fontWeight: 'bold', textTransform: 'uppercase' }}>
                Server Performance
              </Typography>
              <TableContainer sx={{ maxHeight: 300 }}>
                <Table size="small" stickyHeader>
                  <TableHead>
                    <TableRow>
                      <TableCell sx={{ py: 0.5, fontWeight: 'bold', fontSize: '0.75rem' }}>Server</TableCell>
                      <TableCell align="right" sx={{ py: 0.5, fontWeight: 'bold', fontSize: '0.75rem' }}>Priority</TableCell>
                      <TableCell align="right" sx={{ py: 0.5, fontWeight: 'bold', fontSize: '0.75rem' }}>Today</TableCell>
                      <TableCell align="right" sx={{ py: 0.5, fontWeight: 'bold', fontSize: '0.75rem' }}>Week</TableCell>
                      <TableCell align="right" sx={{ py: 0.5, fontWeight: 'bold', fontSize: '0.75rem' }}>Month</TableCell>
                      <TableCell align="right" sx={{ py: 0.5, fontWeight: 'bold', fontSize: '0.75rem' }}>Total</TableCell>
                      {hasArticleStats && (
                        <>
                          <TableCell align="right" sx={{ py: 0.5, fontWeight: 'bold', fontSize: '0.75rem' }}>Articles</TableCell>
                          <TableCell align="right" sx={{ py: 0.5, fontWeight: 'bold', fontSize: '0.75rem' }}>Success</TableCell>
                        </>
                      )}
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {Object.entries(statistics.sabnzbd.servers).map(([serverName, serverData]: [string, any]) => (
                      <TableRow key={serverName} hover sx={{ '&:last-child td': { border: 0 } }}>
                        <TableCell component="th" scope="row" sx={{ py: 0.75 }}>
                          <Typography variant="body2" sx={{ fontWeight: 500, fontSize: '0.8rem' }}>
                            {serverName}
                          </Typography>
                        </TableCell>
                        <TableCell align="right" sx={{ py: 0.75 }}>
                          <Typography variant="body2" sx={{ fontSize: '0.8rem' }}>
                            {serverData.priority ?? 0}
                          </Typography>
                        </TableCell>
                        <TableCell align="right" sx={{ py: 0.75 }}>
                          <Typography variant="body2" sx={{ fontSize: '0.8rem' }}>
                            {formatBytes(serverData.day || 0)}
                          </Typography>
                        </TableCell>
                        <TableCell align="right" sx={{ py: 0.75 }}>
                          <Typography variant="body2" sx={{ fontSize: '0.8rem' }}>
                            {formatBytes(serverData.week || 0)}
                          </Typography>
                        </TableCell>
                        <TableCell align="right" sx={{ py: 0.75 }}>
                          <Typography variant="body2" sx={{ fontSize: '0.8rem' }}>
                            {formatBytes(serverData.month || 0)}
                          </Typography>
                        </TableCell>
                        <TableCell align="right" sx={{ py: 0.75 }}>
                          <Typography variant="body2" sx={{ fontWeight: 500, fontSize: '0.8rem' }}>
                            {formatBytes(serverData.total || 0)}
                          </Typography>
                        </TableCell>
                        {hasArticleStats && (
                          <>
                            <TableCell align="right" sx={{ py: 0.75 }}>
                              {serverData.has_article_stats ? (
                                <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.75rem' }}>
                                  {serverData.articles_success?.toLocaleString() || 0} / {serverData.articles_tried?.toLocaleString() || 0}
                                </Typography>
                              ) : (
                                <Typography variant="caption" color="text.disabled" sx={{ fontSize: '0.75rem' }}>
                                  N/A
                                </Typography>
                              )}
                            </TableCell>
                            <TableCell align="right" sx={{ py: 0.75 }}>
                              {serverData.has_article_stats ? (
                                <Chip
                                  label={`${serverData.success_rate || 0}%`}
                                  size="small"
                                  color={
                                    (serverData.success_rate || 0) > 95 ? 'success' : 
                                    (serverData.success_rate || 0) > 85 ? 'warning' : 'error'
                                  }
                                  sx={{ minWidth: 50, height: 20, fontSize: '0.7rem' }}
                                />
                              ) : (
                                <Typography variant="caption" color="text.disabled" sx={{ fontSize: '0.75rem' }}>
                                  N/A
                                </Typography>
                              )}
                            </TableCell>
                          </>
                        )}
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </>
          ) : (
            <>
              <Divider sx={{ my: 1 }} />
              <Alert severity="info" sx={{ mt: 1 }}>
                No server statistics available. Server stats may not be enabled in SABnzbd or no data has been collected yet.
              </Alert>
            </>
          )}
        </Paper>
      )}

      {/* Prowlarr Statistics */}
      {statistics?.prowlarr?.enabled && !statistics.prowlarr.error && (
        <Paper sx={{ p: 1.5, mb: 1.5 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <SearchIcon sx={{ fontSize: 20, mr: 0.75, color: 'warning.main' }} />
            <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
              Prowlarr
            </Typography>
          </Box>
          <Grid container spacing={1} sx={{ mb: statistics.prowlarr.top_indexers?.length > 0 ? 1.5 : 0 }}>
            <Grid item xs={6} sm={3} md={2}>
              <StatCard
                title="Indexers"
                value={statistics.prowlarr.indexers?.total || 0}
                icon={<SearchIcon fontSize="small" />}
                subtitle={`${statistics.prowlarr.indexers?.enabled || 0} enabled`}
                color="warning"
              />
            </Grid>
            <Grid item xs={6} sm={3} md={2.5}>
              <StatCard
                title="RSS Queries"
                value={statistics.prowlarr.statistics?.total_queries || 0}
                icon={<SearchIcon fontSize="small" />}
                subtitle="Automated"
                color="primary"
                infoTooltip={rssQueriesTooltip}
              />
            </Grid>
            <Grid item xs={6} sm={3} md={2.5}>
              <StatCard
                title="Search Queries"
                value={statistics.prowlarr.statistics?.total_user_queries || 0}
                icon={<SearchIcon fontSize="small" />}
                subtitle="Manual"
                color="secondary"
                infoTooltip={searchQueriesTooltip}
              />
            </Grid>
            <Grid item xs={6} sm={3} md={2}>
              <StatCard
                title="Total Grabs"
                value={statistics.prowlarr.statistics?.total_grabs || 0}
                icon={<DownloadIcon fontSize="small" />}
                subtitle="All sources"
                color="success"
              />
            </Grid>
          </Grid>

          {/* Top Indexers */}
          {statistics.prowlarr.top_indexers && statistics.prowlarr.top_indexers.length > 0 && (
            <>
              <Divider sx={{ my: 1 }} />
              <Typography variant="body2" sx={{ mb: 0.5, display: 'block', fontWeight: 'bold', textTransform: 'uppercase' }}>
                Top Performing Indexers
              </Typography>
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell sx={{ py: 0.5, fontWeight: 'bold', fontSize: '0.8rem' }}>Indexer</TableCell>
                      <TableCell align="right" sx={{ py: 0.5, fontWeight: 'bold', fontSize: '0.8rem' }}>Priority</TableCell>
                      <TableCell align="right" sx={{ py: 0.5, fontWeight: 'bold', fontSize: '0.8rem' }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: 0.5 }}>
                          RSS Queries
                          <Tooltip title={rssQueriesTooltip} arrow placement="top">
                            <InfoIcon sx={{ fontSize: 14, color: 'text.secondary', opacity: 0.6, cursor: 'help' }} />
                          </Tooltip>
                        </Box>
                      </TableCell>
                      <TableCell align="right" sx={{ py: 0.5, fontWeight: 'bold', fontSize: '0.8rem' }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: 0.5 }}>
                          Search Queries
                          <Tooltip title={searchQueriesTooltip} arrow placement="top">
                            <InfoIcon sx={{ fontSize: 14, color: 'text.secondary', opacity: 0.6, cursor: 'help' }} />
                          </Tooltip>
                        </Box>
                      </TableCell>
                      <TableCell align="right" sx={{ py: 0.5, fontWeight: 'bold', fontSize: '0.8rem' }}>Total Grabs</TableCell>
                      <TableCell align="right" sx={{ py: 0.5, fontWeight: 'bold', fontSize: '0.8rem' }}>Avg Response</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {statistics.prowlarr.top_indexers.map((indexer: any, index: number) => (
                      <TableRow key={index} hover sx={{ '&:last-child td': { border: 0 } }}>
                        <TableCell component="th" scope="row" sx={{ py: 0.75 }}>
                          <Typography variant="body2" sx={{ fontWeight: 500, fontSize: '0.9rem' }}>
                            {indexer.name}
                          </Typography>
                        </TableCell>
                        <TableCell align="right" sx={{ py: 0.75 }}>
                          <Typography variant="body2" sx={{ fontSize: '0.9rem' }}>{indexer.priority ?? 25}</Typography>
                        </TableCell>
                        <TableCell align="right" sx={{ py: 0.75 }}>
                          <Typography variant="body2" sx={{ fontSize: '0.9rem' }}>{indexer.queries}</Typography>
                        </TableCell>
                        <TableCell align="right" sx={{ py: 0.75 }}>
                          <Typography variant="body2" sx={{ fontSize: '0.9rem' }}>{indexer.user_queries}</Typography>
                        </TableCell>
                        <TableCell align="right" sx={{ py: 0.75 }}>
                          <Typography variant="body2" sx={{ fontWeight: 500, fontSize: '0.9rem' }}>
                            {indexer.grabs}
                          </Typography>
                        </TableCell>
                        <TableCell align="right" sx={{ py: 0.75 }}>
                          <Typography variant="body2" sx={{ fontSize: '0.9rem' }}>{indexer.avg_response_time}ms</Typography>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </>
          )}
        </Paper>
      )}

      {/* No Integrations */}
      {!statistics?.radarr?.enabled && !statistics?.sonarr?.enabled && 
       !statistics?.sabnzbd?.enabled && !statistics?.prowlarr?.enabled && (
        <Alert severity="info">
          No integrations enabled. Configure in Settings → Integrations.
        </Alert>
      )}

      {/* Errors */}
      {(statistics?.radarr?.error || statistics?.sonarr?.error || 
        statistics?.sabnzbd?.error || statistics?.prowlarr?.error) && (
        <Paper sx={{ p: 1.5, bgcolor: 'error.dark' }}>
          <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 0.5 }}>
            Errors
          </Typography>
          {statistics?.radarr?.error && (
            <Typography variant="caption" display="block">Radarr: {statistics.radarr.error}</Typography>
          )}
          {statistics?.sonarr?.error && (
            <Typography variant="caption" display="block">Sonarr: {statistics.sonarr.error}</Typography>
          )}
          {statistics?.sabnzbd?.error && (
            <Typography variant="caption" display="block">SABnzbd: {statistics.sabnzbd.error}</Typography>
          )}
          {statistics?.prowlarr?.error && (
            <Typography variant="caption" display="block">Prowlarr: {statistics.prowlarr.error}</Typography>
          )}
        </Paper>
      )}

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </Container>
  );
};

export default Statistics;
