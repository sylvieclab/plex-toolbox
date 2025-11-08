import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Breadcrumbs,
  Link,
  Typography,
  CircularProgress,
  Alert,
  Box,
  Chip,
  IconButton,
  Tooltip,
  Snackbar,
  Collapse,
  LinearProgress,
} from '@mui/material';
import {
  Folder as FolderIcon,
  FolderOpen as FolderOpenIcon,
  Home as HomeIcon,
  PlayArrow as ScanIcon,
  Refresh as RefreshIcon,
  ExpandMore as ExpandMoreIcon,
  ExpandLess as ExpandLessIcon,
} from '@mui/icons-material';
import { apiClient } from '../services/api';
import { DirectoryListing, Directory } from '../types';

interface DirectoryBrowserProps {
  open: boolean;
  onClose: () => void;
  libraryKey: string;
  libraryName: string;
  libraryType: string;
  onScanComplete?: () => void;
}

const DirectoryBrowser: React.FC<DirectoryBrowserProps> = ({
  open,
  onClose,
  libraryKey,
  libraryName,
  libraryType,
  onScanComplete,
}) => {
  const [loading, setLoading] = useState(false);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [currentListing, setCurrentListing] = useState<DirectoryListing | null>(null);
  const [currentPath, setCurrentPath] = useState<string>('/');
  const [showActivities, setShowActivities] = useState(false);
  const [activities, setActivities] = useState<any[]>([]);
  const [activityInterval, setActivityInterval] = useState<NodeJS.Timeout | null>(null);

  // Load directories when dialog opens or path changes
  useEffect(() => {
    if (open) {
      loadDirectories(currentPath);
    }
  }, [open, currentPath, libraryKey]);

  // Cleanup activity polling on unmount
  useEffect(() => {
    return () => {
      if (activityInterval) {
        clearInterval(activityInterval);
      }
    };
  }, [activityInterval]);

  const loadDirectories = async (path: string) => {
    setLoading(true);
    setError(null);
    try {
      const listing = await apiClient.getLibraryDirectories(libraryKey, path);
      setCurrentListing(listing);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to load directories');
    } finally {
      setLoading(false);
    }
  };

  const loadActivities = async () => {
    try {
      const data = await apiClient.getPlexActivities();
      setActivities(data.activities);
    } catch (err) {
      console.error('Failed to load activities:', err);
    }
  };

  const startActivityPolling = () => {
    // Load immediately
    loadActivities();
    // Then poll every 2 seconds
    const interval = setInterval(loadActivities, 2000);
    setActivityInterval(interval);
  };

  const stopActivityPolling = () => {
    if (activityInterval) {
      clearInterval(activityInterval);
      setActivityInterval(null);
    }
  };

  const handleRefresh = () => {
    loadDirectories(currentPath);
  };

  const handleNavigate = (path: string) => {
    setCurrentPath(path);
  };

  const handleNavigateUp = () => {
    if (currentListing && currentListing.parent_path !== null) {
      setCurrentPath(currentListing.parent_path || '/');
    }
  };

  const handleScanDirectory = async (path?: string) => {
    setScanning(true);
    setError(null);
    setShowActivities(true);
    startActivityPolling();
    
    try {
      const result = await apiClient.scanLibraryPath(libraryKey, path || undefined);
      setSuccessMessage(
        `${result.scan_type === 'partial' ? 'Partial' : 'Full'} scan completed! ` +
        `Duration: ${result.duration_seconds?.toFixed(2) || 'N/A'}s`
      );
      onScanComplete?.();
      // Refresh the current directory to show any new folders
      setTimeout(() => {
        handleRefresh();
        stopActivityPolling();
      }, 3000);
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Failed to start scan');
      stopActivityPolling();
    } finally {
      setScanning(false);
    }
  };

  const getBreadcrumbs = () => {
    if (!currentListing) return [];
    
    const parts = currentListing.current_path.split('/').filter(p => p);
    const breadcrumbs = [
      { label: libraryName, path: '/' }
    ];
    
    let accumulatedPath = '';
    for (const part of parts) {
      accumulatedPath += '/' + part;
      breadcrumbs.push({
        label: part,
        path: accumulatedPath
      });
    }
    
    return breadcrumbs;
  };

  return (
    <>
      <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
        <DialogTitle>
          <Box display="flex" alignItems="center" justifyContent="space-between">
            <Typography variant="h6">Browse &amp; Scan Directory</Typography>
            <Box display="flex" alignItems="center" gap={1}>
              <Tooltip title="Refresh directory listing">
                <IconButton 
                  onClick={handleRefresh} 
                  disabled={loading}
                  size="small"
                  color="primary"
                >
                  {loading ? <CircularProgress size={20} /> : <RefreshIcon />}
                </IconButton>
              </Tooltip>
              <Chip 
                label={libraryType} 
                size="small" 
                color="primary" 
                variant="outlined"
              />
            </Box>
          </Box>
        </DialogTitle>

        <DialogContent>
          {/* Breadcrumb navigation */}
          <Box mb={2}>
            <Breadcrumbs>
              {getBreadcrumbs().map((crumb, index) => (
                <Link
                  key={index}
                  component="button"
                  variant="body2"
                  onClick={() => handleNavigate(crumb.path)}
                  sx={{
                    cursor: 'pointer',
                    textDecoration: index === getBreadcrumbs().length - 1 ? 'none' : 'underline',
                    color: index === getBreadcrumbs().length - 1 ? 'text.primary' : 'primary.main',
                  }}
                >
                  {index === 0 && <HomeIcon sx={{ mr: 0.5, fontSize: 16, verticalAlign: 'middle' }} />}
                  {crumb.label}
                </Link>
              ))}
            </Breadcrumbs>
          </Box>

          {/* Scan Activity Feed */}
          {showActivities && (
            <Box mb={2}>
              <Button
                fullWidth
                onClick={() => setShowActivities(!showActivities)}
                endIcon={showActivities ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                sx={{ justifyContent: 'space-between', mb: 1 }}
              >
                Plex Activity Feed ({activities.length})
              </Button>
              <Collapse in={showActivities}>
                <Box sx={{ 
                  border: '1px solid #e0e0e0', 
                  borderRadius: 1, 
                  maxHeight: '200px', 
                  overflow: 'auto',
                  bgcolor: 'background.paper'
                }}>
                  {activities.length === 0 ? (
                    <Box p={2} textAlign="center">
                      <Typography variant="body2" color="text.secondary">
                        No active scan operations
                      </Typography>
                    </Box>
                  ) : (
                    <List dense>
                      {activities.map((activity, index) => (
                        <ListItem key={activity.uuid || index}>
                          <ListItemText
                            primary={activity.title}
                            secondary={
                              <Box>
                                {activity.subtitle && (
                                  <Typography variant="caption" display="block">
                                    {activity.subtitle}
                                  </Typography>
                                )}
                                {activity.progress !== undefined && activity.progress > 0 && (
                                  <LinearProgress 
                                    variant="determinate" 
                                    value={activity.progress} 
                                    sx={{ mt: 0.5 }}
                                  />
                                )}
                              </Box>
                            }
                          />
                        </ListItem>
                      ))}
                    </List>
                  )}
                </Box>
              </Collapse>
            </Box>
          )}

          {/* Error display */}
          {error && (
            <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError(null)}>
              {error}
            </Alert>
          )}

          {/* Loading state */}
          {loading && (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
              <CircularProgress />
            </Box>
          )}

          {/* Directory list */}
          {!loading && currentListing && (
            <Box>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                <Typography variant="body2" color="text.secondary">
                  {currentListing.directories.length} {currentListing.directories.length === 1 ? 'folder' : 'folders'}
                </Typography>
                <Button
                  variant="contained"
                  size="small"
                  startIcon={<ScanIcon />}
                  onClick={() => handleScanDirectory(currentListing.current_path)}
                  disabled={scanning}
                >
                  {scanning ? 'Scanning...' : 'Scan This Folder'}
                </Button>
              </Box>

              <List sx={{ maxHeight: '400px', overflow: 'auto', border: '1px solid #e0e0e0', borderRadius: 1 }}>
                {/* Parent directory option */}
                {currentListing.parent_path !== null && (
                  <ListItem disablePadding>
                    <ListItemButton onClick={handleNavigateUp}>
                      <ListItemIcon>
                        <FolderOpenIcon />
                      </ListItemIcon>
                      <ListItemText 
                        primary=".." 
                        secondary="Parent directory"
                      />
                    </ListItemButton>
                  </ListItem>
                )}

                {/* Directory list */}
                {currentListing.directories.length === 0 && currentListing.parent_path === null && (
                  <ListItem>
                    <ListItemText 
                      primary="No subdirectories found" 
                      secondary="This is the library root or an empty directory"
                    />
                  </ListItem>
                )}

                {currentListing.directories.map((dir: Directory) => (
                  <ListItem key={dir.path} disablePadding>
                    <ListItemButton onClick={() => handleNavigate(dir.path)}>
                      <ListItemIcon>
                        <FolderIcon color="primary" />
                      </ListItemIcon>
                      <ListItemText primary={dir.name} />
                    </ListItemButton>
                  </ListItem>
                ))}
              </List>
            </Box>
          )}
        </DialogContent>

        <DialogActions>
          <Button onClick={onClose} disabled={scanning}>
            Close
          </Button>
          <Button 
            onClick={() => handleScanDirectory()} 
            variant="outlined"
            startIcon={<ScanIcon />}
            disabled={scanning}
          >
            {scanning ? 'Scanning...' : 'Scan Entire Library'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Success notification */}
      <Snackbar
        open={!!successMessage}
        autoHideDuration={6000}
        onClose={() => setSuccessMessage(null)}
        message={successMessage}
      />
    </>
  );
};

export default DirectoryBrowser;
