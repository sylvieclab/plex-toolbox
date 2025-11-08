/**
 * TypeScript type definitions for Plex Toolbox
 */

export interface PlexServerConfig {
  url: string;
  token: string;
}

export interface PlexServerInfo {
  name: string;
  version: string;
  platform: string;
  platform_version: string;
  machine_identifier: string;
}

export interface PlexLibrary {
  key: string;
  title: string;
  type: string;
  agent?: string;
  scanner?: string;
  language?: string;
  uuid: string;
  updated_at?: string;
  created_at?: string;
  scanned_at?: string;
  total_items: number;
}

export interface LibraryScanRequest {
  library_key: string;
  path?: string;
}

export interface LibraryScanResponse {
  status: string;
  library_key: string;
  library_name: string;
  message: string;
  started_at: string;
}

export interface PlexMediaItem {
  key: string;
  title: string;
  type: string;
  year?: number;
  rating?: number;
  summary?: string;
  thumb?: string;
  art?: string;
  duration?: number;
  added_at?: string;
  updated_at?: string;
}

export interface LibraryStats {
  library_key: string;
  library_name: string;
  library_type: string;
  total_items: number;
  total_duration_minutes: number;
  recently_added_count: number;
  last_scanned?: string;
}

export interface ScanHistory {
  id: number;
  library_key: string;
  library_name: string;
  library_type: string;
  scan_type: 'full' | 'partial';
  path?: string;
  status: 'started' | 'completed' | 'failed';
  started_at: string;
  completed_at?: string;
  duration_seconds?: number;
  error_message?: string;
}

export interface ScanHistoryResponse {
  scans: ScanHistory[];
  total: number;
}

export interface Directory {
  name: string;
  path: string;
  full_path: string;
  is_directory: boolean;
}

export interface DirectoryListing {
  library_key: string;
  library_name: string;
  current_path: string;
  parent_path: string | null;
  directories: Directory[];
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}

export interface DashboardStats {
  total_libraries: number;
  total_items: number;
  by_type: {
    movie: number;
    show: number;
    artist: number;
    photo: number;
    other: number;
  };
  last_scan: string | null;
  recent_scans: number;
}

export interface RecentItem {
  title: string;
  type: string;
  library: string;
  added_at: string | null;
  year?: number;
  rating?: number;
  thumb?: string | null;
}

export interface RecentItemsResponse {
  items: RecentItem[];
}

export interface ServerStatus {
  connected: boolean;
  server_name: string | null;
  version: string | null;
  response_time_ms: number | null;
  error?: string;
}

// Integration types
export type IntegrationServiceType = 'sonarr' | 'radarr' | 'sabnzbd' | 'prowlarr';

export interface IntegrationConfig {
  id?: number;
  service_type: IntegrationServiceType;
  name: string;
  url: string;
  api_key: string;
  enabled: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface IntegrationTestRequest {
  service_type: IntegrationServiceType;
  url: string;
  api_key: string;
}

export interface IntegrationTestResponse {
  success: boolean;
  message: string;
  version?: string;
  error?: string;
}

// SABnzbd types
export interface SabnzbdQueueSlot {
  nzo_id: string;
  filename: string;
  mb: string;
  mbleft: string;
  percentage: string;
  eta: string;
  status: string;
  timeleft: string;
}

export interface SabnzbdQueue {
  queue: {
    paused: boolean;
    speed: string;
    sizeleft: string;
    size: string;
    eta: string;
    slots: SabnzbdQueueSlot[];
  };
}

export interface SabnzbdHistoryItem {
  nzo_id: string;
  name: string;
  status: string;
  bytes: string;
  fail_message?: string;
  completed?: number;
}

export interface SabnzbdHistory {
  history: {
    slots: SabnzbdHistoryItem[];
  };
}

export interface SabnzbdStatus {
  paused: boolean;
  speed: string;
  size_left: string;
  size: string;
  eta: string;
  disk_space: string;
  slots: number;
}

// Sonarr types
export interface SonarrSeries {
  id: number;
  title: string;
  overview?: string;
  year?: number;
  status?: string;
  images?: any[];
  seasons?: any[];
}

export interface SonarrEpisode {
  id: number;
  seriesId: number;
  episodeNumber: number;
  seasonNumber: number;
  title: string;
  airDateUtc?: string;
  hasFile: boolean;
}

export interface SonarrMissing {
  records: SonarrEpisode[];
  page: number;
  pageSize: number;
  totalRecords: number;
}

export interface SonarrQueue {
  records: any[];
  totalRecords: number;
}

// Radarr types
export interface RadarrMovie {
  id: number;
  title: string;
  overview?: string;
  year?: number;
  status?: string;
  hasFile: boolean;
  monitored: boolean;
  images?: any[];
}

export interface RadarrQueue {
  records: any[];
  totalRecords: number;
}

// Prowlarr types
export interface ProwlarrIndexer {
  id: number;
  name: string;
  enable: boolean;
  protocol: string;
  privacy: string;
  priority: number;
}

export interface ProwlarrStats {
  indexers: Array<{
    indexerId: number;
    indexerName: string;
    averageResponseTime: number;
    numberOfQueries: number;
    numberOfGrabs: number;
    numberOfFailedQueries: number;
  }>;
}
