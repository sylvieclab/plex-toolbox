import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  MenuItem,
  Alert,
  Box,
  CircularProgress,
  FormControlLabel,
  Switch,
} from '@mui/material';
import { apiClient } from '../../services/api';
import { IntegrationConfig, IntegrationServiceType } from '../../types';

interface IntegrationDialogProps {
  open: boolean;
  integration: IntegrationConfig | null;
  onClose: () => void;
  onSave: () => void;
}

const IntegrationDialog = ({
  open,
  integration,
  onClose,
  onSave,
}: IntegrationDialogProps) => {
  const [formData, setFormData] = useState<Partial<IntegrationConfig>>({
    service_type: 'sabnzbd',
    name: '',
    url: '',
    api_key: '',
    enabled: true,
  });
  const [testing, setTesting] = useState(false);
  const [saving, setSaving] = useState(false);
  const [testResult, setTestResult] = useState<{
    success: boolean;
    message: string;
    version?: string;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (integration) {
      setFormData(integration);
    } else {
      setFormData({
        service_type: 'sabnzbd',
        name: '',
        url: '',
        api_key: '',
        enabled: true,
      });
    }
    setTestResult(null);
    setError(null);
  }, [integration, open]);

  const handleChange = (field: keyof IntegrationConfig, value: any) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    setTestResult(null); // Clear test result when form changes
  };

  const handleTest = async () => {
    setTesting(true);
    setTestResult(null);
    setError(null);

    try {
      const result = await apiClient.testIntegration({
        service_type: formData.service_type,
        url: formData.url,
        api_key: formData.api_key,
      });
      setTestResult(result);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Connection test failed');
      setTestResult({ success: false, message: 'Connection test failed' });
    } finally {
      setTesting(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setError(null);

    try {
      if (integration?.id) {
        // Update existing
        await apiClient.updateIntegration(integration.id, formData);
      } else {
        // Create new
        await apiClient.createIntegration(formData);
      }
      onSave();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save integration');
    } finally {
      setSaving(false);
    }
  };

  const isFormValid = () => {
    return (
      formData.service_type &&
      formData.name &&
      formData.url &&
      formData.api_key
    );
  };

  const serviceTypes: Array<{ value: IntegrationServiceType; label: string }> = [
    { value: 'sabnzbd', label: 'SABnzbd' },
    { value: 'sonarr', label: 'Sonarr' },
    { value: 'radarr', label: 'Radarr' },
    { value: 'prowlarr', label: 'Prowlarr' },
  ];

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        {integration ? 'Edit Integration' : 'Add Integration'}
      </DialogTitle>
      <DialogContent>
        <Box sx={{ pt: 2 }}>
          <TextField
            select
            fullWidth
            label="Service Type"
            value={formData.service_type}
            onChange={(e) =>
              handleChange('service_type', e.target.value as IntegrationServiceType)
            }
            disabled={!!integration}
            sx={{ mb: 2 }}
          >
            {serviceTypes.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>

          <TextField
            fullWidth
            label="Name"
            value={formData.name}
            onChange={(e) => handleChange('name', e.target.value)}
            placeholder="e.g., Main SABnzbd"
            sx={{ mb: 2 }}
          />

          <TextField
            fullWidth
            label="URL"
            value={formData.url}
            onChange={(e) => handleChange('url', e.target.value)}
            placeholder="http://localhost:8080"
            sx={{ mb: 2 }}
          />

          <TextField
            fullWidth
            label="API Key"
            value={formData.api_key}
            onChange={(e) => handleChange('api_key', e.target.value)}
            type="password"
            sx={{ mb: 2 }}
          />

          <FormControlLabel
            control={
              <Switch
                checked={formData.enabled}
                onChange={(e) => handleChange('enabled', e.target.checked)}
              />
            }
            label="Enabled"
          />

          <Box sx={{ mt: 2, mb: 2 }}>
            <Button
              variant="outlined"
              onClick={handleTest}
              disabled={!isFormValid() || testing}
              fullWidth
            >
              {testing ? <CircularProgress size={24} /> : 'Test Connection'}
            </Button>
          </Box>

          {testResult && (
            <Alert severity={testResult.success ? 'success' : 'error'} sx={{ mb: 2 }}>
              {testResult.message}
              {testResult.version && ` (Version: ${testResult.version})`}
            </Alert>
          )}

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          variant="contained"
          onClick={handleSave}
          disabled={!isFormValid() || saving}
        >
          {saving ? <CircularProgress size={24} /> : 'Save'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default IntegrationDialog;
