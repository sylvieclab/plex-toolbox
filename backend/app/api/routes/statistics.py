"""
API routes for aggregate statistics across all integrations
Provides comprehensive statistics for the Statistics page
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from loguru import logger
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.integrations import IntegrationConfig
from app.services.integrations import RadarrClient, SonarrClient, SabnzbdClient, ProwlarrClient

router = APIRouter(prefix="/statistics", tags=["statistics"])


def get_enabled_integration(db: Session, service_type: str) -> Optional[IntegrationConfig]:
    """Get an enabled integration config"""
    return (
        db.query(IntegrationConfig)
        .filter(
            IntegrationConfig.service_type == service_type,
            IntegrationConfig.enabled == True
        )
        .first()
    )


async def get_radarr_statistics(db: Session) -> Optional[Dict[str, Any]]:
    """Get Radarr statistics"""
    config = get_enabled_integration(db, "radarr")
    if not config:
        return None
    
    try:
        client = RadarrClient(config.url, config.api_key)
        
        # Get all movies
        movies = await client.get_movies()
        
        # Get queue
        queue_data = await client.get_queue()
        queue = queue_data.get("records", [])
        
        # Get disk space
        try:
            disk_space_data = await client._request("GET", "/api/v3/diskspace")
        except:
            disk_space_data = []
        
        # Calculate statistics
        total_movies = len(movies)
        monitored_movies = sum(1 for m in movies if m.get("monitored"))
        unmonitored_movies = total_movies - monitored_movies
        downloaded_movies = sum(1 for m in movies if m.get("hasFile"))
        missing_movies = sum(1 for m in movies if m.get("monitored") and not m.get("hasFile"))
        
        # Calculate total size
        total_size = sum(m.get("sizeOnDisk", 0) for m in movies)
        
        # Group by quality
        quality_breakdown = {}
        for movie in movies:
            if movie.get("hasFile"):
                quality_profile_id = movie.get("qualityProfileId", 0)
                quality_breakdown[quality_profile_id] = quality_breakdown.get(quality_profile_id, 0) + 1
        
        # Calculate disk space
        total_disk_space = sum(d.get("totalSpace", 0) for d in disk_space_data)
        free_disk_space = sum(d.get("freeSpace", 0) for d in disk_space_data)
        
        return {
            "enabled": True,
            "service": "Radarr",
            "movies": {
                "total": total_movies,
                "monitored": monitored_movies,
                "unmonitored": unmonitored_movies,
                "downloaded": downloaded_movies,
                "missing": missing_movies,
                "download_percentage": round((downloaded_movies / total_movies * 100) if total_movies > 0 else 0, 1)
            },
            "storage": {
                "total_size": total_size,
                "total_size_gb": round(total_size / (1024**3), 2),
                "disk_total": total_disk_space,
                "disk_free": free_disk_space,
                "disk_used_percentage": round(((total_disk_space - free_disk_space) / total_disk_space * 100) if total_disk_space > 0 else 0, 1)
            },
            "queue": {
                "total_items": len(queue),
                "downloading": sum(1 for q in queue if q.get("status") == "downloading"),
                "queued": sum(1 for q in queue if q.get("status") == "queued")
            },
            "quality_breakdown": quality_breakdown
        }
    except Exception as e:
        logger.error(f"Failed to get Radarr statistics: {str(e)}")
        return {"enabled": True, "error": str(e)}


async def get_sonarr_statistics(db: Session) -> Optional[Dict[str, Any]]:
    """Get Sonarr statistics"""
    config = get_enabled_integration(db, "sonarr")
    if not config:
        return None
    
    try:
        client = SonarrClient(config.url, config.api_key)
        
        # Get all series
        series_list = await client.get_series()
        
        # Get queue
        queue_data = await client.get_queue()
        queue = queue_data.get("records", [])
        
        # Get disk space
        try:
            disk_space_data = await client._request("GET", "/api/v3/diskspace")
        except:
            disk_space_data = []
        
        # Calculate statistics
        total_series = len(series_list)
        monitored_series = sum(1 for s in series_list if s.get("monitored"))
        continuing_series = sum(1 for s in series_list if s.get("status") == "continuing")
        ended_series = sum(1 for s in series_list if s.get("status") == "ended")
        
        # Episode statistics
        total_episodes = sum(s.get("statistics", {}).get("episodeCount", 0) for s in series_list)
        downloaded_episodes = sum(s.get("statistics", {}).get("episodeFileCount", 0) for s in series_list)
        missing_episodes = total_episodes - downloaded_episodes
        
        # Calculate total size
        total_size = sum(s.get("statistics", {}).get("sizeOnDisk", 0) for s in series_list)
        
        # Calculate disk space
        total_disk_space = sum(d.get("totalSpace", 0) for d in disk_space_data)
        free_disk_space = sum(d.get("freeSpace", 0) for d in disk_space_data)
        
        return {
            "enabled": True,
            "service": "Sonarr",
            "series": {
                "total": total_series,
                "monitored": monitored_series,
                "continuing": continuing_series,
                "ended": ended_series
            },
            "episodes": {
                "total": total_episodes,
                "downloaded": downloaded_episodes,
                "missing": missing_episodes,
                "download_percentage": round((downloaded_episodes / total_episodes * 100) if total_episodes > 0 else 0, 1)
            },
            "storage": {
                "total_size": total_size,
                "total_size_gb": round(total_size / (1024**3), 2),
                "disk_total": total_disk_space,
                "disk_free": free_disk_space,
                "disk_used_percentage": round(((total_disk_space - free_disk_space) / total_disk_space * 100) if total_disk_space > 0 else 0, 1)
            },
            "queue": {
                "total_items": len(queue),
                "downloading": sum(1 for q in queue if q.get("status") == "downloading"),
                "queued": sum(1 for q in queue if q.get("status") == "queued")
            }
        }
    except Exception as e:
        logger.error(f"Failed to get Sonarr statistics: {str(e)}")
        return {"enabled": True, "error": str(e)}


def safe_int(value: Any, default: int = 0) -> int:
    """Safely convert a value to int, handling strings, floats, and dicts"""
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return default
    return default


async def get_sabnzbd_statistics(db: Session) -> Optional[Dict[str, Any]]:
    """Get SABnzbd statistics with per-server breakdown including priority"""
    config = get_enabled_integration(db, "sabnzbd")
    if not config:
        return None
    
    try:
        client = SabnzbdClient(config.url, config.api_key)
        
        # Get queue
        queue_data = await client.get_queue()
        queue = queue_data.get("queue", {})
        
        # Get history with statistics
        history_data = await client.get_history(limit=100)
        history = history_data.get("history", {})
        
        # Get SABnzbd config to get server priorities
        server_priorities = {}
        try:
            config_data = await client._request(
                "GET",
                "/api",
                params={"mode": "get_config", "output": "json"}
            )
            # Parse server configuration for priorities
            servers_config = config_data.get("config", {}).get("servers", [])
            for server in servers_config:
                server_name = server.get("host", "")
                if server_name:
                    server_priorities[server_name] = server.get("priority", 0)
            logger.debug(f"SABnzbd server priorities: {server_priorities}")
        except Exception as e:
            logger.warning(f"Failed to get SABnzbd config for priorities: {str(e)}")
        
        # Get server stats - this includes per-server breakdown
        # Note: This endpoint may not be available on all SABnzbd installations
        servers = {}
        total_bytes = 0
        day_bytes = 0
        week_bytes = 0
        month_bytes = 0
        
        try:
            server_stats_raw = await client.get_server_stats()
            logger.info(f"SABnzbd server_stats response type: {type(server_stats_raw)}")
            logger.debug(f"SABnzbd server_stats response: {server_stats_raw}")
            
            # Handle different response formats
            if isinstance(server_stats_raw, dict):
                # Try direct access first for overall stats
                total_bytes = safe_int(server_stats_raw.get("total", 0))
                day_bytes = safe_int(server_stats_raw.get("day", 0))
                week_bytes = safe_int(server_stats_raw.get("week", 0))
                month_bytes = safe_int(server_stats_raw.get("month", 0))
                
                # Extract per-server stats
                reserved_keys = {"total", "month", "week", "day", "servers"}
                
                # Check if there's a 'servers' key (some SABnzbd versions use this)
                servers_data = server_stats_raw.get("servers", server_stats_raw)
                
                for key, value in servers_data.items():
                    if key not in reserved_keys and isinstance(value, dict):
                        server_name = key
                        server_data = value
                        
                        # Safely extract numeric values
                        day_val = safe_int(server_data.get("day", 0))
                        week_val = safe_int(server_data.get("week", 0))
                        month_val = safe_int(server_data.get("month", 0))
                        total_val = safe_int(server_data.get("total", 0))
                        articles_tried = safe_int(server_data.get("articles_tried", 0))
                        articles_success = safe_int(server_data.get("articles_success", 0))
                        
                        # Calculate success rate - only if articles were tried
                        success_rate = round((articles_success / articles_tried * 100) if articles_tried > 0 else 0, 1)
                        
                        # Get priority for this server
                        priority = server_priorities.get(server_name, 0)
                        
                        servers[server_name] = {
                            "day": day_val,
                            "week": week_val,
                            "month": month_val,
                            "total": total_val,
                            "articles_tried": articles_tried,
                            "articles_success": articles_success,
                            "success_rate": success_rate,
                            "has_article_stats": articles_tried > 0,  # Flag to show if article stats are available
                            "priority": priority  # Server priority
                        }
                        
                        # If we didn't get overall stats, calculate from servers
                        if total_bytes == 0:
                            total_bytes += total_val
                            day_bytes += day_val
                            week_bytes += week_val
                            month_bytes += month_val
                
                logger.info(f"Parsed {len(servers)} SABnzbd servers from stats")
        except Exception as e:
            logger.warning(f"Failed to get SABnzbd server stats (this is optional): {str(e)}")
            # Server stats are optional, continue without them
        
        # Parse queue data
        queue_slots = queue.get("slots", [])
        speed = queue.get("kbpersec", "0")
        
        # Parse history statistics (these are just formatted strings)
        day_size = history.get("day_size", "0 B")
        week_size = history.get("week_size", "0 B")
        month_size = history.get("month_size", "0 B")
        total_size = history.get("total_size", "0 B")
        
        # Get recent history
        history_slots = history.get("slots", [])[:10]
        recent_downloads = []
        for slot in history_slots:
            recent_downloads.append({
                "name": slot.get("name", "Unknown"),
                "status": slot.get("status", "Unknown"),
                "size": slot.get("size", "0 B"),
                "completed": slot.get("completed", 0)
            })
        
        return {
            "enabled": True,
            "service": "SABnzbd",
            "queue": {
                "active_downloads": len(queue_slots),
                "speed_kbps": float(speed) if speed else 0,
                "speed_mbps": round(float(speed) / 1024, 2) if speed else 0,
                "size_left": queue.get("sizeleft", "0 B"),
                "size_left_mb": round(float(queue.get("mbleft", 0)), 2),
                "eta": queue.get("timeleft", "unknown"),
                "paused": queue.get("paused", False)
            },
            "statistics": {
                "day_size": day_size,
                "week_size": week_size,
                "month_size": month_size,
                "total_size": total_size,
                "day_bytes": day_bytes,
                "week_bytes": week_bytes,
                "month_bytes": month_bytes,
                "total_bytes": total_bytes,
                "day_gb": round(day_bytes / (1024**3), 2) if day_bytes else 0,
                "week_gb": round(week_bytes / (1024**3), 2) if week_bytes else 0,
                "month_gb": round(month_bytes / (1024**3), 2) if month_bytes else 0,
                "total_gb": round(total_bytes / (1024**3), 2) if total_bytes else 0
            },
            "servers": servers,  # Per-server breakdown (may be empty)
            "recent_downloads": recent_downloads,
            "disk_space": {
                "free": queue.get("diskspace1", "unknown"),
                "total": queue.get("diskspacetotal1", "unknown")
            }
        }
    except Exception as e:
        logger.error(f"Failed to get SABnzbd statistics: {str(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return {"enabled": True, "error": str(e)}


async def get_prowlarr_statistics(db: Session) -> Optional[Dict[str, Any]]:
    """Get Prowlarr statistics including indexer priorities"""
    config = get_enabled_integration(db, "prowlarr")
    if not config:
        return None
    
    try:
        client = ProwlarrClient(config.url, config.api_key)
        
        # Get indexers (this includes priority information)
        indexers = await client.get_indexers()
        
        # Create a mapping of indexer ID to priority
        indexer_priorities = {idx.get("id"): idx.get("priority", 25) for idx in indexers}
        logger.debug(f"Prowlarr indexer priorities: {indexer_priorities}")
        
        # Get indexer statistics
        try:
            stats = await client.get_indexer_stats()
            logger.debug(f"Prowlarr stats response: {stats}")
        except Exception as e:
            logger.warning(f"Failed to get Prowlarr stats: {str(e)}")
            stats = {"indexers": []}
        
        # Calculate statistics
        total_indexers = len(indexers)
        enabled_indexers = sum(1 for i in indexers if i.get("enable", False))
        disabled_indexers = total_indexers - enabled_indexers
        
        # Parse indexer stats
        indexer_stats = stats.get("indexers", [])
        
        # Calculate totals across different query types
        # IMPORTANT: Based on actual Prowlarr API response:
        # numberOfQueries = Manual search queries (user-initiated)
        # numberOfRssQueries = RSS queries (automated)
        total_rss_queries = sum(s.get("numberOfRssQueries", 0) for s in indexer_stats)
        total_search_queries = sum(s.get("numberOfQueries", 0) for s in indexer_stats)
        total_grabs = sum(s.get("numberOfGrabs", 0) for s in indexer_stats)
        
        # Get top performing indexers by grabs
        top_indexers = sorted(
            indexer_stats,
            key=lambda x: x.get("numberOfGrabs", 0),
            reverse=True
        )[:5]
        
        top_indexers_formatted = []
        for idx in top_indexers:
            # Get different query counts
            num_rss_queries = idx.get("numberOfRssQueries", 0)  # RSS queries (automated)
            num_search_queries = idx.get("numberOfQueries", 0)  # Manual search queries
            num_grabs = idx.get("numberOfGrabs", 0)
            indexer_id = idx.get("indexerId", 0)
            
            # Get priority from indexers list
            priority = indexer_priorities.get(indexer_id, 25)
            
            top_indexers_formatted.append({
                "name": idx.get("indexerName", "Unknown"),
                "queries": num_rss_queries,  # RSS queries (automated)
                "user_queries": num_search_queries,  # Search queries (manual)
                "grabs": num_grabs,  # Total grabs (RSS + manual)
                "avg_response_time": idx.get("averageResponseTime", 0),
                "priority": priority  # Indexer priority
            })
        
        return {
            "enabled": True,
            "service": "Prowlarr",
            "indexers": {
                "total": total_indexers,
                "enabled": enabled_indexers,
                "disabled": disabled_indexers
            },
            "statistics": {
                "total_queries": total_rss_queries,  # RSS queries (automated)
                "total_user_queries": total_search_queries,  # Search queries (manual)
                "total_grabs": total_grabs,  # Total grabs
            },
            "top_indexers": top_indexers_formatted
        }
    except Exception as e:
        logger.error(f"Failed to get Prowlarr statistics: {str(e)}")
        return {"enabled": True, "error": str(e)}


@router.get("/overview")
async def get_statistics_overview(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get comprehensive statistics overview from all enabled integrations
    
    Returns aggregated statistics from Radarr, Sonarr, SABnzbd, and Prowlarr
    """
    try:
        # Gather statistics from all services
        radarr_stats = await get_radarr_statistics(db)
        sonarr_stats = await get_sonarr_statistics(db)
        sabnzbd_stats = await get_sabnzbd_statistics(db)
        prowlarr_stats = await get_prowlarr_statistics(db)
        
        # Calculate time ranges for display
        now = datetime.utcnow()
        time_ranges = {
            "today": {
                "start": now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat(),
                "end": now.isoformat(),
                "label": "Today"
            },
            "week": {
                "start": (now - timedelta(days=7)).isoformat(),
                "end": now.isoformat(),
                "label": "Last 7 Days"
            },
            "month": {
                "start": (now - timedelta(days=30)).isoformat(),
                "end": now.isoformat(),
                "label": "Last 30 Days"
            },
            "all_time": {
                "label": "All Time"
            }
        }
        
        return {
            "timestamp": now.isoformat(),
            "time_ranges": time_ranges,
            "radarr": radarr_stats,
            "sonarr": sonarr_stats,
            "sabnzbd": sabnzbd_stats,
            "prowlarr": prowlarr_stats
        }
    except Exception as e:
        logger.error(f"Failed to get statistics overview: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get statistics: {str(e)}"
        )


@router.get("/radarr")
async def get_radarr_stats_endpoint(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get detailed Radarr statistics"""
    stats = await get_radarr_statistics(db)
    if stats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Radarr integration not enabled"
        )
    return stats


@router.get("/sonarr")
async def get_sonarr_stats_endpoint(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get detailed Sonarr statistics"""
    stats = await get_sonarr_statistics(db)
    if stats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sonarr integration not enabled"
        )
    return stats


@router.get("/sabnzbd")
async def get_sabnzbd_stats_endpoint(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get detailed SABnzbd statistics"""
    stats = await get_sabnzbd_statistics(db)
    if stats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SABnzbd integration not enabled"
        )
    return stats


@router.get("/prowlarr")
async def get_prowlarr_stats_endpoint(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get detailed Prowlarr statistics"""
    stats = await get_prowlarr_statistics(db)
    if stats is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prowlarr integration not enabled"
        )
    return stats
