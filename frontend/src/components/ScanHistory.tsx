import { useState, useEffect } from 'react';
import {
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  Typography,
  IconButton,
  Tooltip,
  CircularProgress,
} from '@mui/material';
import { Delete, CheckCircle, Error, HourglassEmpty, FolderOpen, LibraryBooks } from '@mui/icons-material';
import { apiClient } from '../services/api';
import { ScanHistory as ScanHistoryType } from '../types';

interface ScanHistoryProps {
  libraryKey?: string;
  limit?: number;
}

const ScanHistory = ({ libraryKey, limit = 20 }: ScanHistoryProps) => {
  const [scans, setScans] = useState<ScanHistoryType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHistory();
  }, [libraryKey, limit]);

  const fetchHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiClient.getScanHistory(libraryKey, limit);
      setScans(data.scans);
    } catch (err) {
      console.error('Failed to fetch scan history:', err);
      setError('Failed to load scan history');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (scanId: number) => {
    try {
      await apiClient.deleteScanHistory(scanId);
      fetchHistory();
    } catch (err) {
      console.error('Failed to delete scan:', err);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle color="success" />;
      case 'failed':
        return <Error color="error" />;
      case 'started':
        return <HourglassEmpty color="warning" />;
      default:
        return null;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'failed':
        return 'error';
      case 'started':
        return 'warning';
      default:
        return 'default';
    }
  };
  
  const getScanTypeColor = (scanType: string) => {
    return scanType === 'partial' ? 'secondary' : 'primary';
  };

  const formatDuration = (seconds?: number) => {
    if (!seconds) return 'N/A';
    if (seconds < 60) return `${Math.round(seconds)}s`;
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.round(seconds % 60);
    return `${minutes}m ${remainingSeconds}s`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString();
  };
  
  const truncatePath = (path?: string, maxLength: number = 30) => {
    if (!path) return 'Entire library';
    if (path.length <= maxLength) return path;
    return '...' + path.slice(-maxLength);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box p={2}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  if (scans.length === 0) {
    return (
      <Box p={2}>
        <Typography color="text.secondary">No scan history found</Typography>
      </Box>
    );
  }

  return (
    <TableContainer component={Paper} sx={{ maxHeight: 500 }}>
      <Table stickyHeader>
        <TableHead>
          <TableRow>
            <TableCell>Library</TableCell>
            <TableCell>Scope</TableCell>
            <TableCell>Path</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Started</TableCell>
            <TableCell>Duration</TableCell>
            <TableCell align="center">Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {scans.map((scan) => (
            <TableRow key={scan.id} hover>
              <TableCell>
                <Typography variant="body2" fontWeight="medium">
                  {scan.library_name}
                </Typography>
                <Chip 
                  label={scan.library_type} 
                  size="small" 
                  variant="outlined"
                  sx={{ mt: 0.5 }}
                />
              </TableCell>
              <TableCell>
                <Chip 
                  icon={scan.scan_type === 'partial' ? <FolderOpen /> : <LibraryBooks />}
                  label={scan.scan_type === 'partial' ? 'Partial' : 'Full'} 
                  size="small"
                  color={getScanTypeColor(scan.scan_type) as any}
                  variant="filled"
                />
              </TableCell>
              <TableCell>
                <Tooltip title={scan.path || 'Entire library'}>
                  <Typography variant="body2" sx={{ fontFamily: 'monospace', fontSize: '0.75rem' }}>
                    {truncatePath(scan.path)}
                  </Typography>
                </Tooltip>
              </TableCell>
              <TableCell>
                <Box display="flex" alignItems="center" gap={1}>
                  {getStatusIcon(scan.status)}
                  <Chip 
                    label={scan.status} 
                    size="small"
                    color={getStatusColor(scan.status) as any}
                  />
                </Box>
              </TableCell>
              <TableCell>
                <Typography variant="body2">
                  {formatDate(scan.started_at)}
                </Typography>
              </TableCell>
              <TableCell>
                <Typography variant="body2" fontWeight={scan.scan_type === 'partial' ? 'bold' : 'normal'}>
                  {formatDuration(scan.duration_seconds)}
                </Typography>
              </TableCell>
              <TableCell align="center">
                <Tooltip title="Delete">
                  <IconButton
                    size="small"
                    onClick={() => handleDelete(scan.id)}
                    color="error"
                  >
                    <Delete />
                  </IconButton>
                </Tooltip>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ScanHistory;
