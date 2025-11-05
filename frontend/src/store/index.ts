/**
 * Zustand store for application state management
 */
import { create } from 'zustand';
import { PlexServerInfo, PlexLibrary } from '../types';
import { apiClient } from '../services/api';

interface AppState {
  // Plex server state
  plexConnected: boolean;
  plexServerInfo: PlexServerInfo | null;
  setPlexConnected: (connected: boolean) => void;
  setPlexServerInfo: (info: PlexServerInfo | null) => void;
  checkPlexConnection: () => Promise<void>;

  // Libraries state
  libraries: PlexLibrary[];
  selectedLibrary: PlexLibrary | null;
  setLibraries: (libraries: PlexLibrary[]) => void;
  setSelectedLibrary: (library: PlexLibrary | null) => void;

  // UI state
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  loading: boolean;
  setLoading: (loading: boolean) => void;
}

export const useAppStore = create<AppState>((set) => ({
  // Plex server state
  plexConnected: false,
  plexServerInfo: null,
  setPlexConnected: (connected) => set({ plexConnected: connected }),
  setPlexServerInfo: (info) => set({ plexServerInfo: info }),
  
  // Check if Plex is configured in backend
  checkPlexConnection: async () => {
    try {
      const config = await apiClient.getPlexConfig();
      if (config.configured) {
        set({ 
          plexConnected: true,
          plexServerInfo: config.server_name ? {
            name: config.server_name,
            version: config.version || '',
            platform: config.platform || '',
            platform_version: '',
            machine_identifier: '',
          } : null
        });
      }
    } catch (error) {
      console.error('Failed to check Plex connection:', error);
      set({ plexConnected: false, plexServerInfo: null });
    }
  },

  // Libraries state
  libraries: [],
  selectedLibrary: null,
  setLibraries: (libraries) => set({ libraries }),
  setSelectedLibrary: (library) => set({ selectedLibrary: library }),

  // UI state
  sidebarOpen: true,
  setSidebarOpen: (open) => set({ sidebarOpen: open }),
  loading: false,
  setLoading: (loading) => set({ loading }),
}));
