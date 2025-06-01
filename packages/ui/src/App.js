import React, { useState, useEffect } from 'react';
import { Box, Container, CircularProgress, Alert } from '@mui/material';
import ChatInterface from './components/Chat/ChatInterface';
import { checkApiHealth } from './services/api';

function App() {
  const [apiStatus, setApiStatus] = useState({
    isChecking: true,
    isHealthy: false,
    error: null
  });

  // Check API health on component mount
  useEffect(() => {
    const checkHealth = async () => {
      try {
        await checkApiHealth();
        setApiStatus({
          isChecking: false,
          isHealthy: true,
          error: null
        });
      } catch (error) {
        setApiStatus({
          isChecking: false,
          isHealthy: false,
          error: 'API is not available. Please ensure the API server is running.'
        });
      }
    };

    checkHealth();
  }, []);

  return (
    <Box sx={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {apiStatus.isChecking ? (
        <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
          <CircularProgress />
        </Container>
      ) : apiStatus.isHealthy ? (
        <ChatInterface />
      ) : (
        <Container sx={{ mt: 4 }}>
          <Alert severity="error">
            {apiStatus.error}
          </Alert>
        </Container>
      )}
    </Box>
  );
}

export default App;
