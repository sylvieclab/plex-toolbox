# Plex Toolbox 🎬

Advanced management tools for Plex Media Server

## 🌟 Current Status

**Version**: 0.1.0  
**Status**: ✅ Active Development - Priority 1 Complete!

### ✅ Working Features
- **Database Persistence** - Configure once, works forever
- **Plex Server Connection** - Automatic reconnection on startup
- **Library Management** - View and scan all your libraries
- **Dashboard** - Server information and statistics
- **Modern UI** - Dark theme matching Plex aesthetic

### 🚧 In Development
- Enhanced Libraries Page (Priority 2)
- Scan History Tracking (Priority 3)  
- Dashboard Enhancements (Priority 4)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Plex Media Server with authentication token

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd plex-toolbox
   ```

2. **Start the application**
   ```bash
   start-simple.bat
   ```
   *For Linux/Mac, see `Claude_Docs/QUICK_START.md`*

3. **Configure Plex**
   - Open http://localhost:3000
   - Enter your Plex server URL and token
   - Configuration persists automatically!

### Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs

---

## 🎯 Planned Features

### Phase 1: Core Features (Current)
- ✅ **Database Persistence** - Configuration management
- 🔄 **Enhanced Libraries** - Better UI and filtering
- ⏳ **Scan History** - Track all library scans
- ⏳ **Dashboard Stats** - More useful information

### Phase 2: Advanced Features
- 🔮 **Duplicate Media Finder** - Find and remove duplicates
- 🔮 **Metadata Management** - Bulk edit metadata and artwork
- 🔮 **User Activity** - Track what's being watched
- 🔮 **Selective Scanning** - Scan specific shows or seasons

### Phase 3: Automation
- 🔮 **Scheduled Scans** - Automatic recurring scans
- 🔮 **Auto-Organization** - Rules-based file management
- 🔮 **Notifications** - Email/Discord/Slack alerts

### Phase 4: Integrations
- 🔮 **Sonarr/Radarr** - *arr stack integration
- 🔮 **Overseerr** - Request management
- 🔮 **Webhooks** - Custom event triggers

---

## 📚 Documentation

### For Users
- **[Quick Start Guide](Claude_Docs/QUICK_START.md)** - Get up and running
- **[API Reference](Claude_Docs/API_REFERENCE.md)** - All endpoints documented
- **[Troubleshooting](Claude_Docs/TROUBLESHOOTING.md)** - Common issues

### For Developers
- **[Development Roadmap](Claude_Docs/NEXT_SESSION_ROADMAP.md)** - Next steps
- **[Session Summary](Claude_Docs/SESSION_COMPLETE_2025-11-04.md)** - Recent changes
- **[Project Structure](Claude_Docs/PROJECT_STRUCTURE.md)** - Architecture overview

---

## 🛠️ Technology Stack

**Backend**
- FastAPI - Modern Python web framework
- SQLAlchemy - Database ORM
- PlexAPI - Plex server integration
- SQLite - Local database

**Frontend**
- React 18 - UI framework
- TypeScript - Type safety
- Material-UI - Component library
- Zustand - State management

---

## 🔧 Development

### Start Development Environment
```bash
# Backend (Terminal 1)
cd backend
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/Mac
uvicorn app.main:app --reload

# Frontend (Terminal 2)
cd frontend
npm start
```

### Project Structure
```
plex-toolbox/
├── backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── models/   # Database models
│   │   └── services/ # Business logic
│   └── plex_toolbox.db  # SQLite database
├── frontend/         # React TypeScript frontend
│   └── src/
│       ├── pages/    # Page components
│       ├── components/ # Reusable components
│       └── store/    # State management
└── Claude_Docs/      # Development documentation
```

---

## 🐛 Troubleshooting

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
del plex_toolbox.db  # Windows
rm plex_toolbox.db   # Linux/Mac
# Restart backend - database will recreate
```

---

## 🤝 Contributing

This is a personal project in active development. Feel free to:
- Report issues
- Suggest features
- Submit pull requests

See `Claude_Docs/NEXT_SESSION_ROADMAP.md` for planned features and priorities.

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- **Plex** - For the amazing media server
- **PlexAPI** - Python library for Plex integration
- **FastAPI** - Modern Python web framework
- **React** - UI library
- **Material-UI** - Component library

---

## 📞 Support

For issues or questions:
1. Check the documentation in `Claude_Docs/`
2. Review API docs at http://localhost:8000/api/docs
3. Check browser console for frontend errors
4. Review backend logs in `backend/logs/`

---

**Built with ❤️ for Plex enthusiasts**

*Last Updated: 2025-11-04*  
*Status: Priority 1 Complete - Database Persistence Working!*
