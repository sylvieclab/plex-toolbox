# Totarr

Advanced management and monitoring for Plex, Jellyfin, and the *arr ecosystem (Radarr, Sonarr, SABnzbd, Prowlarr)

## Current Status

**Version**: 0.3.0  
**Status**: Active Development - Priorities 1-3 Complete

### Working Features
- Database Persistence - Configure once, works forever
- Enhanced Libraries Page - Search, filter, sort with beautiful cards
- Scan History Tracking - Complete history of all library scans
- Library Management - View and scan all your libraries
- Statistics Dashboard - Real-time monitoring of all *arr services
- Integration Management - Centralized control of Radarr, Sonarr, SABnzbd, Prowlarr
- Modern UI - Dark theme matching Plex aesthetic

### Planned Features
- Dashboard Enhancements (Priority 4)
- Advanced Scanning Features (Priority 5)
- Jellyfin Integration
- Historical Statistics & Trends

---

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Plex Media Server with authentication token
- Optional: Radarr, Sonarr, SABnzbd, Prowlarr

### Installation

1. Clone the repository
   ```bash
   git clone <your-repo-url>
   cd totarr
   ```

2. Start the application
   ```bash
   start-simple.bat
   ```

3. Configure Services
   - Open http://localhost:3000
   - Enter your Plex server URL and token
   - Add your *arr integrations (optional)
   - Configuration persists automatically

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs

---

## Features

### Phase 1: Core Features (Current)
- ✓ Database Persistence - Configuration management
- ✓ Enhanced Libraries - Search, filter, sort with visual cards
- ✓ Scan History - Track all library scans with status
- ✓ Statistics Dashboard - Real-time monitoring across all services
- ✓ Integration Management - Centralized *arr app control
- Planned: Dashboard Stats - Overview and quick actions

### Phase 2: Advanced Features
- Scan Completion Tracking - Real-time scan progress
- Directory Scanning - Scan specific folders
- Duplicate Media Finder - Find and remove duplicates
- Metadata Management - Bulk edit metadata and artwork
- Historical Statistics - Time-series data with TimescaleDB

### Phase 3: Automation
- Scheduled Scans - Automatic recurring scans
- Auto-Organization - Rules-based file management
- Notifications - Email/Discord/Slack alerts

### Phase 4: Integrations
- Jellyfin - Complete Jellyfin support
- Overseerr - Request management
- Webhooks - Custom event triggers

---

## Technology Stack

### Backend
- FastAPI - Modern Python web framework
- SQLAlchemy - Database ORM
- PlexAPI - Plex server integration
- SQLite/PostgreSQL - Database options
- TimescaleDB - Time-series statistics (optional)

### Frontend
- React 18 - UI framework
- TypeScript - Type safety
- Material-UI - Component library
- Axios - HTTP client

---

## Development

### Start Development Environment

**Backend (Terminal 1)**
```bash
cd backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
uvicorn app.main:app --reload
```

**Frontend (Terminal 2)**
```bash
cd frontend
npm start
```

### Project Structure
```
totarr/
├── backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── models/   # Database models
│   │   └── services/ # Business logic
│   └── totarr.db     # SQLite database
└── frontend/         # React TypeScript frontend
    └── src/
        ├── pages/    # Page components
        ├── components/ # Reusable components
        └── services/ # API client
```

---

## Troubleshooting

### Backend Issues
```bash
cd backend
pip install -r requirements.txt --break-system-packages
```

### Frontend Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Database Issues
```bash
cd backend
del totarr.db  # Windows
rm totarr.db   # Linux/Mac
# Restart backend - database will recreate
```

For more help, check the API documentation at http://localhost:8000/api/docs

---

## Contributing

This is a personal project in active development. Feel free to:
- Report issues
- Suggest features
- Submit pull requests

---

## License

MIT License - See LICENSE file for details

---

## Acknowledgments

- **Plex** - For the amazing media server
- **Jellyfin** - Open-source media system
- **PlexAPI** - Python library for Plex integration
- **The *arr Community** - Radarr, Sonarr, Prowlarr, and all the automation tools
- **FastAPI** - Modern Python web framework
- **React** - UI library
- **Material-UI** - Component library

---

## Support

For issues or questions:
1. Check the API docs at http://localhost:8000/api/docs
2. Check browser console (F12) for frontend errors
3. Review backend logs in `backend/logs/`

---

**Built for media enthusiasts and self-hosters**

*Last Updated: 2025-11-08*  
*Version: 0.3.0*  
*Status: Priorities 1-3 Complete - Working Application*
