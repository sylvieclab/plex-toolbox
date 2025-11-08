import {
  Card,
  CardContent,
  Box,
  Typography,
  IconButton,
  Chip,
  Stack,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { IntegrationConfig } from '../../types';

interface IntegrationCardProps {
  integration: IntegrationConfig;
  onEdit: () => void;
  onDelete: () => void;
  onToggleEnabled: () => void;
}

const IntegrationCard = ({
  integration,
  onEdit,
  onDelete,
  onToggleEnabled,
}: IntegrationCardProps) => {
  return (
    <Card sx={{ mb: 2 }}>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start">
          <Box flex={1}>
            <Typography variant="h6" gutterBottom>
              {integration.name}
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {integration.url}
            </Typography>
            <Stack direction="row" spacing={1} mt={1}>
              <Chip
                label={integration.enabled ? 'Enabled' : 'Disabled'}
                color={integration.enabled ? 'success' : 'default'}
                size="small"
                onClick={onToggleEnabled}
                sx={{ cursor: 'pointer' }}
              />
              <Chip
                label={`API: ${integration.api_key}`}
                size="small"
                variant="outlined"
              />
            </Stack>
          </Box>
          <Box>
            <IconButton size="small" onClick={onEdit} title="Edit">
              <EditIcon fontSize="small" />
            </IconButton>
            <IconButton size="small" onClick={onDelete} title="Delete" color="error">
              <DeleteIcon fontSize="small" />
            </IconButton>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default IntegrationCard;
