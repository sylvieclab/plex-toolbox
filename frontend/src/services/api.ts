/**
 * API client for Plex Toolbox backend
 */
import axios, { AxiosInstance } from 'axios';
import {
  PlexServerConfig,
  PlexLibrary,
  PlexMediaItem,
  LibraryStats,
  ScanHistoryResponse,
  DashboardStats,
  RecentItemsResponse,
  ServerStatus,
  DirectoryListing,
} from '../types';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Health check
  async healthCheck() {
    const response = await this.client.get('/health');
    return response.data;
  }

  // Plex connection
  async connectToPlex(config: PlexServerConfig) {
    const response = await this.client.post<{ success: boolean; server_name?: string; version?: string; platform?: string; error?: string }>(
      '/plex/test-connection',
      config
    );
    return response.data;
  }

  async savePlexConfig(config: PlexServerConfig) {
    const response = await this.client.post('/plex/config', config);
    return response.data;
  }

  async getPlexConfig() {
    const response = await this.client.get('/plex/config');
    return response.data;
  }

  async getServerInfo() {
    const response = await this.client.get('/plex/server-info');
    return response.data;
  }

  // Library management
  async getLibraries(): Promise<PlexLibrary[]> {
    const response = await this.client.get<{ libraries: PlexLibrary[] }>('/plex/libraries');
    return response.data.libraries;
  }

  async getLibraryDetails(libraryKey: string): Promise<PlexLibrary> {
    const response = await this.client.get<PlexLibrary>(`/library/libraries/${libraryKey}`);
    return response.data;
  }

  async getLibraryContent(
    libraryKey: string,
    limit: number = 50,
    offset: number = 0
  ): Promise<{ items: PlexMediaItem[]; total: number; has_more: boolean }> {
    const response = await this.client.get(`/library/libraries/${libraryKey}/content`, {
      params: { limit, offset },
    });
    return response.data;
  }

  async getLibraryStats(libraryKey: string): Promise<LibraryStats> {
    const response = await this.client.get<LibraryStats>(
      `/library/libraries/${libraryKey}/stats`
    );
    return response.data;
  }

  async scanLibrary(libraryKey: string): Promise<{ status: string; message: string }> {
    const response = await this.client.post(`/plex/libraries/${libraryKey}/scan`);
    return response.data;
  }

  // Directory browsing
  async getLibraryDirectories(
    libraryKey: string,
    path: string = '/'
  ): Promise<DirectoryListing> {
    const response = await this.client.get<DirectoryListing>(
      `/library/libraries/${libraryKey}/directories`,
      { params: { path } }
    );
    return response.data;
  }

  // Scan with optional path
  async scanLibraryPath(
    libraryKey: string,
    path?: string
  ): Promise<{ 
    status: string; 
    message: string;
    scan_id: number;
    scan_type: string;
    path?: string;
    library_key: string;
    library_name: string;
    started_at: string;
    completed_at?: string;
    duration_seconds?: number;
  }> {
    const response = await this.client.post(
      `/scan/libraries/${libraryKey}/scan`,
      { path }
    );
    return response.data;
  }

  // Scan history
  async getScanHistory(libraryKey?: string, limit: number = 50): Promise<ScanHistoryResponse> {
    const params = new URLSearchParams();
    params.append('limit', limit.toString());
    if (libraryKey) {
      params.append('library_key', libraryKey);
    }
    
    const response = await this.client.get<ScanHistoryResponse>(
      `/scan/scan-history?${params.toString()}`
    );
    return response.data;
  }

  async deleteScanHistory(scanId: number): Promise<{ status: string; message: string }> {
    const response = await this.client.delete(`/scan/scan-history/${scanId}`);
    return response.data;
  }

  async scanLibraryWithHistory(libraryKey: string): Promise<{ 
    status: string; 
    message: string;
    scan_id: number;
    started_at: string;
    completed_at?: string;
  }> {
    const response = await this.client.post(`/scan/libraries/${libraryKey}/scan`);
    return response.data;
  }

  // Dashboard
  async getDashboardStats(): Promise<DashboardStats> {
    const response = await this.client.get<DashboardStats>('/dashboard/stats');
    return response.data;
  }

  async getRecentItems(): Promise<RecentItemsResponse> {
    const response = await this.client.get<RecentItemsResponse>('/dashboard/recent');
    return response.data;
  }

  async getServerStatus(): Promise<ServerStatus> {
    const response = await this.client.get<ServerStatus>('/dashboard/server-status');
    return response.data;
  }

  // Plex activities
  async getPlexActivities(): Promise<{ activities: any[] }> {
    const response = await this.client.get('/scan/plex-activities');
    return response.data;
  }

  // Integration Management
  async testIntegration(data: any): Promise<any> {
    const response = await this.client.post('/integrations/test', data);
    return response.data;
  }

  async createIntegration(data: any): Promise<any> {
    const response = await this.client.post('/integrations', data);
    return response.data;
  }

  async getIntegrations(serviceType?: string): Promise<any[]> {
    const params = serviceType ? { service_type: serviceType } : {};
    const response = await this.client.get('/integrations', { params });
    return response.data;
  }

  async getIntegration(id: number): Promise<any> {
    const response = await this.client.get(`/integrations/${id}`);
    return response.data;
  }

  async updateIntegration(id: number, data: any): Promise<any> {
    const response = await this.client.put(`/integrations/${id}`, data);
    return response.data;
  }

  async deleteIntegration(id: number): Promise<void> {
    await this.client.delete(`/integrations/${id}`);
  }

  // SABnzbd
  async getSabnzbdQueue(): Promise<any> {
    const response = await this.client.get('/sabnzbd/queue');
    return response.data;
  }

  async getSabnzbdHistory(limit: number = 50): Promise<any> {
    const response = await this.client.get('/sabnzbd/history', { params: { limit } });
    return response.data;
  }

  async pauseSabnzbd(): Promise<any> {
    const response = await this.client.post('/sabnzbd/pause');
    return response.data;
  }

  async resumeSabnzbd(): Promise<any> {
    const response = await this.client.post('/sabnzbd/resume');
    return response.data;
  }

  async getSabnzbdStatus(): Promise<any> {
    const response = await this.client.get('/sabnzbd/status');
    return response.data;
  }

  // Sonarr
  async getSonarrSeries(): Promise<any[]> {
    const response = await this.client.get('/sonarr/series');
    return response.data;
  }

  async getSonarrMissing(page: number = 1, pageSize: number = 50): Promise<any> {
    const response = await this.client.get('/sonarr/missing', { params: { page, page_size: pageSize } });
    return response.data;
  }

  async searchSonarrEpisodes(episodeIds: number[]): Promise<any> {
    const response = await this.client.post('/sonarr/search', episodeIds);
    return response.data;
  }

  async getSonarrQueue(): Promise<any> {
    const response = await this.client.get('/sonarr/queue');
    return response.data;
  }

  // Radarr
  async getRadarrMovies(): Promise<any[]> {
    const response = await this.client.get('/radarr/movies');
    return response.data;
  }

  async getRadarrMissing(): Promise<any[]> {
    const response = await this.client.get('/radarr/missing');
    return response.data;
  }

  async searchRadarrMovies(movieIds: number[]): Promise<any> {
    const response = await this.client.post('/radarr/search', movieIds);
    return response.data;
  }

  async getRadarrQueue(): Promise<any> {
    const response = await this.client.get('/radarr/queue');
    return response.data;
  }

  // Prowlarr
  async getProwlarrIndexers(): Promise<any[]> {
    const response = await this.client.get('/prowlarr/indexers');
    return response.data;
  }

  async getProwlarrStats(): Promise<any> {
    const response = await this.client.get('/prowlarr/stats');
    return response.data;
  }

  async testProwlarrIndexer(indexerId: number): Promise<any> {
    const response = await this.client.post(`/prowlarr/test/${indexerId}`);
    return response.data;
  }
}

export const apiClient = new ApiClient();
