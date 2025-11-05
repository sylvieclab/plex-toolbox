import { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box, CircularProgress } from '@mui/material';
import { useAppStore } from './store';

// Placeholder pages - will create these next
import Dashboard from './pages/Dashboard';
import Setup from './pages/Setup';
import Libraries from './pages/Libraries';
import Settings from './pages/Settings';

// Placeholder layout component
import Layout from './components/common/Layout';

function App() {
  const { plexConnected, loading, setLoading, checkPlexConnection } = useAppStore();

  useEffect(() => {
    // Check if Plex is already configured on app startup
    const initializeApp = async () => {
      setLoading(true);
      await checkPlexConnection();
      setLoading(false);
    };
    
    initializeApp();
  }, [checkPlexConnection, setLoading]);

  // Show loading spinner while checking configuration
  if (loading) {
    return (
      <Box 
        sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center', 
          minHeight: '100vh' 
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      {!plexConnected ? (
        // If not connected, show setup page
        <Routes>
          <Route path="/setup" element={<Setup />} />
          <Route path="*" element={<Navigate to="/setup" replace />} />
        </Routes>
      ) : (
        // If connected, show main application
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/libraries" element={<Libraries />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Layout>
      )}
    </Box>
  );
}

export default App;
