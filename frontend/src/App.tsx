import { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box, CircularProgress } from '@mui/material';
import { useAppStore } from './store';

import Dashboard from './pages/Dashboard';
import Setup from './pages/Setup';
import Libraries from './pages/Libraries';
import Settings from './pages/Settings';
import Integrations from './pages/Integrations';
import Statistics from './pages/Statistics';
import Layout from './components/common/Layout';

function App() {
  const { plexConnected, loading, setLoading, checkPlexConnection } = useAppStore();

  useEffect(() => {
    const initializeApp = async () => {
      setLoading(true);
      await checkPlexConnection();
      setLoading(false);
    };
    
    initializeApp();
  }, [checkPlexConnection, setLoading]);

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
        <Routes>
          <Route path="/setup" element={<Setup />} />
          <Route path="*" element={<Navigate to="/setup" replace />} />
        </Routes>
      ) : (
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/libraries" element={<Libraries />} />
            <Route path="/statistics" element={<Statistics />} />
            <Route path="/integrations" element={<Integrations />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Layout>
      )}
    </Box>
  );
}

export default App;
