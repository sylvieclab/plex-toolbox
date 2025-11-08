import { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  Chip,
  CircularProgress,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  InputAdornment,
  Alert,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Refresh,
  Movie,
  Tv,
  LibraryMusic,
  Photo,
  Search as SearchIcon,
  Storage,
  History,
  FolderOpen,
} from '@mui/icons-material';
import { apiClient } from '../services/api';
import { PlexLibrary } from '../types';
import ScanHistory from '../components/ScanHistory';
import DirectoryBrowser from '../components/DirectoryBrowser';

const Libraries = () => {
  const [libraries, setLibraries] = useState<PlexLibrary[]>([]);
  const [filteredLibraries, setFilteredLibraries] = useState<PlexLibrary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [scanningLibraries, setScanningLibraries] = useState<Set<string>>(new Set());
  const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);
  
  // Filter and sort states
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [sortBy, setSortBy] = useState('name');
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());
  
  // History modal states
  const [historyModalOpen, setHistoryModalOpen] = useState(false);
  const [selectedLibraryKey, setSelectedLibraryKey] = useState<string | undefined>();
  const [selectedLibraryName, setSelectedLibraryName] = useState<string>('');
  
  // Directory browser states
  const [browserModalOpen, setBrowserModalOpen] = useState(false);
  const [browserLibraryKey, setBrowserLibraryKey] = useState<string>('');
  const [browserLibraryName, setBrowserLibraryName] = useState<string>('');
  const [browserLibraryType, setBrowserLibraryType] = useState<string>('');

  // Fetch libraries on mount
  useEffect(() => {
    fetchLibraries();
  }, []);

  // Apply filters and sorting whenever libraries or filters change
  useEffect(() => {
    applyFiltersAndSort();
  }, [libraries, searchQuery, filterType, sortBy]);

  const fetchLibraries = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient.getLibraries();
      setLibraries(data);
      setLastUpdated(new Date());
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch libraries');
    } finally {
      setLoading(false);
    }
  };

  const applyFiltersAndSort = () => {
    let filtered = [...libraries];

    // Apply search filter
    if (searchQuery) {
      filtered = filtered.filter(lib =>
        lib.title.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Apply type filter
    if (filterType !== 'all') {
      filtered = filtered.filter(lib => lib.type === filterType);
    }

    // Apply sorting
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return a.title.localeCompare(b.title);
        case 'items':
          return (b.total_items || 0) - (a.total_items || 0);
        case 'updated':
          const dateA = a.updated_at ? new Date(a.updated_at).getTime() : 0;
          const dateB = b.updated_at ? new Date(b.updated_at).getTime() : 0;
          return dateB - dateA;
        default:
          return 0;
      }
    });

    setFilteredLibraries(filtered);
  };

  const handleScan = async (library: PlexLibrary) => {
    setScanningLibraries(prev => new Set(prev).add(library.key));
    setNotification(null);

    try {
      const result = await apiClient.scanLibraryWithHistory(library.key);
      setNotification({
        type: 'success',
        message: `Scan ${result.status} for ${library.title}`,
      });

      // Refresh library list after 3 seconds
      setTimeout(() => {
        fetchLibraries();
      }, 3000);
    } catch (err: any) {
      setNotification({
        type: 'error',
        message: `Failed to scan ${library.title}: ${err.response?.data?.detail || err.message}`,
      });
    } finally {
      setScanningLibraries(prev => {
        const next = new Set(prev);
        next.delete(library.key);
        return next;
      });
    }
  };
  
  const handleOpenBrowser = (library: PlexLibrary) => {
    setBrowserLibraryKey(library.key);
    setBrowserLibraryName(library.title);
    setBrowserLibraryType(library.type);
    setBrowserModalOpen(true);
  };
  
  const handleScanComplete = () => {
    fetchLibraries();
    setNotification({
      type: 'success',
      message: 'Scan completed successfully!',
    });
  };

  const getLibraryIcon = (type: string) => {
    const iconProps = { fontSize: 'large' as const, sx: { color: getLibraryColor(type) } };
    switch (type) {
      case 'movie':
        return <Movie {...iconProps} />;
      case 'show':
        return <Tv {...iconProps} />;
      case 'artist':
        return <LibraryMusic {...iconProps} />;
      case 'photo':
        return <Photo {...iconProps} />;
      default:
        return <Storage {...iconProps} />;
    }
  };

  const getLibraryColor = (type: string): string => {
    switch (type) {
      case 'movie':
        return '#e8a87c'; // Plex orange
      case 'show':
        return '#cc7b19'; // Plex gold
      case 'artist':
        return '#9b59b6'; // Purple
      case 'photo':
        return '#3498db'; // Blue
      default:
        return '#95a5a6'; // Gray
    }
  };

  const getLibraryTypeLabel = (type: string): string => {
    switch (type) {
      case 'movie':
        return 'Movies';
      case 'show':
        return 'TV Shows';
      case 'artist':
        return 'Music';
      case 'photo':
        return 'Photos';
      default:
        return type;
    }
  };

  const formatTimestamp = (timestamp?: string): string => {
    if (!timestamp) return 'Never';
    
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    
    return date.toLocaleDateString();
  };

  if (loading && libraries.length === 0) {
    return (
      <Container maxWidth="lg">
        <Box sx={{ py: 4, display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '400px' }}>
          <CircularProgress />
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        {/* Header */}
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Box>
            <Typography variant="h4" gutterBottom>
              Libraries
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Manage your Plex libraries • Last updated: {formatTimestamp(lastUpdated.toISOString())}
            </Typography>
          </Box>
          <Tooltip title="Refresh libraries">
            <IconButton
              onClick={fetchLibraries}
              disabled={loading}
              color="primary"
              size="large"
            >
              {loading ? <CircularProgress size={24} /> : <Refresh />}
            </IconButton>
          </Tooltip>
        </Box>

        {/* Notification */}
        {notification && (
          <Alert
            severity={notification.type}
            onClose={() => setNotification(null)}
            sx={{ mb: 3 }}
          >
            {notification.message}
          </Alert>
        )}

        {/* Error Message */}
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {/* Filters and Search */}
        <Box display="flex" gap={2} mb={3} flexWrap="wrap">
          <TextField
            placeholder="Search libraries..."
            size="small"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            sx={{ minWidth: 250 }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
          />

          <FormControl size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Type</InputLabel>
            <Select
              value={filterType}
              label="Type"
              onChange={(e) => setFilterType(e.target.value)}
            >
              <MenuItem value="all">All Types</MenuItem>
              <MenuItem value="movie">Movies</MenuItem>
              <MenuItem value="show">TV Shows</MenuItem>
              <MenuItem value="artist">Music</MenuItem>
              <MenuItem value="photo">Photos</MenuItem>
            </Select>
          </FormControl>

          <FormControl size="small" sx={{ minWidth: 150 }}>
            <InputLabel>Sort By</InputLabel>
            <Select
              value={sortBy}
              label="Sort By"
              onChange={(e) => setSortBy(e.target.value)}
            >
              <MenuItem value="name">Name</MenuItem>
              <MenuItem value="items">Items Count</MenuItem>
              <MenuItem value="updated">Last Updated</MenuItem>
            </Select>
          </FormControl>
        </Box>

        {/* Libraries Grid */}
        {filteredLibraries.length === 0 ? (
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <Typography variant="h6" color="text.secondary" gutterBottom>
              {searchQuery || filterType !== 'all' 
                ? 'No libraries match your filters'
                : 'No libraries found'}
            </Typography>
            {(searchQuery || filterType !== 'all') && (
              <Button
                variant="outlined"
                onClick={() => {
                  setSearchQuery('');
                  setFilterType('all');
                }}
                sx={{ mt: 2 }}
              >
                Clear Filters
              </Button>
            )}
          </Box>
        ) : (
          <Box
            sx={{
              display: 'grid',
              gridTemplateColumns: {
                xs: '1fr',
                sm: 'repeat(2, 1fr)',
                md: 'repeat(3, 1fr)',
              },
              gap: 3,
            }}
          >
            {filteredLibraries.map((library) => {
              const isScanning = scanningLibraries.has(library.key);
              
              return (
                <Card
                  key={library.key}
                  sx={{
                    borderLeft: '4px solid',
                    borderColor: getLibraryColor(library.type),
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: 6,
                    },
                  }}
                >
                  <CardContent>
                    {/* Header */}
                    <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                      <Box display="flex" alignItems="center" gap={2}>
                        {getLibraryIcon(library.type)}
                        <Box>
                          <Typography variant="h6" component="div">
                            {library.title}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {getLibraryTypeLabel(library.type)}
                            {library.language && ` • ${library.language}`}
                          </Typography>
                        </Box>
                      </Box>
                    </Box>

                    {/* Stats */}
                    <Box mb={2}>
                      <Chip
                        label={`${(library.total_items || 0).toLocaleString()} items`}
                        color="primary"
                        size="small"
                        sx={{ mr: 1 }}
                      />
                    </Box>

                    {/* Metadata */}
                    <Box mb={2}>
                      {library.updated_at && (
                        <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                          Last scanned: {formatTimestamp(library.updated_at)}
                        </Typography>
                      )}
                      {library.scanner && (
                        <Typography variant="caption" color="text.secondary">
                          Scanner: {library.scanner}
                        </Typography>
                      )}
                    </Box>

                    {/* Actions */}
                    <Box display="flex" flexDirection="column" gap={1}>
                      <Box display="flex" gap={1}>
                        <Button
                          variant="outlined"
                          startIcon={isScanning ? <CircularProgress size={16} /> : <Refresh />}
                          onClick={() => handleScan(library)}
                          disabled={isScanning}
                          fullWidth
                          sx={{
                            borderColor: getLibraryColor(library.type),
                            color: getLibraryColor(library.type),
                            '&:hover': {
                              borderColor: getLibraryColor(library.type),
                              backgroundColor: `${getLibraryColor(library.type)}20`,
                            },
                          }}
                        >
                          {isScanning ? 'Scanning...' : 'Scan All'}
                        </Button>
                        <Button
                          variant="text"
                          size="small"
                          startIcon={<History />}
                          onClick={() => {
                            setSelectedLibraryKey(library.key);
                            setSelectedLibraryName(library.title);
                            setHistoryModalOpen(true);
                          }}
                        >
                          History
                        </Button>
                      </Box>
                      <Button
                        variant="contained"
                        startIcon={<FolderOpen />}
                        onClick={() => handleOpenBrowser(library)}
                        fullWidth
                        sx={{
                          backgroundColor: getLibraryColor(library.type),
                          '&:hover': {
                            backgroundColor: getLibraryColor(library.type),
                            filter: 'brightness(0.9)',
                          },
                        }}
                      >
                        Browse & Scan
                      </Button>
                    </Box>
                  </CardContent>
                </Card>
              );
            })}
          </Box>
        )}

        {/* Summary */}
        {filteredLibraries.length > 0 && (
          <Box sx={{ mt: 4, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              Showing {filteredLibraries.length} of {libraries.length} libraries
              {libraries.length > 0 && (
                <> • Total items: {libraries.reduce((sum, lib) => sum + (lib.total_items || 0), 0).toLocaleString()}</>
              )}
            </Typography>
          </Box>
        )}
      </Box>

      {/* Scan History Modal */}
      <Dialog
        open={historyModalOpen}
        onClose={() => setHistoryModalOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Scan History
          {selectedLibraryName && (
            <Typography variant="body2" color="text.secondary">
              {selectedLibraryName}
            </Typography>
          )}
        </DialogTitle>
        <DialogContent>
          <ScanHistory libraryKey={selectedLibraryKey} />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setHistoryModalOpen(false)}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
      
      {/* Directory Browser Modal */}
      <DirectoryBrowser
        open={browserModalOpen}
        onClose={() => setBrowserModalOpen(false)}
        libraryKey={browserLibraryKey}
        libraryName={browserLibraryName}
        libraryType={browserLibraryType}
        onScanComplete={handleScanComplete}
      />
    </Container>
  );
};

export default Libraries;
