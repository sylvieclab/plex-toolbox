# 🎉 Welcome to Totarr!

**Your central hub for managing Plex, Jellyfin, and the entire *arr ecosystem**

---

## 🌟 What is Totarr?

**Totarr** (pronounced "toe-tar") is a unified web application that brings together all your media management and automation services into one beautiful, easy-to-use interface.

### Why "Totarr"?
- **Tot** = "All" or "Whole" (from Latin/Germanic roots)
- **arr** = Following the beloved *arr naming convention
- **Together** = "All your *arr apps in one place"

---

## 🎯 What Does It Do?

Totarr gives you **one dashboard** to:

### Media Servers
- ✅ **Plex** - Monitor libraries, scan content, view history
- 🔄 **Jellyfin** - Coming soon!

### *arr Automation Stack
- ✅ **Radarr** - Movie collection management
- ✅ **Sonarr** - TV show management  
- ✅ **Prowlarr** - Indexer management
- ✅ **SABnzbd** - Download client monitoring

### Features
- 📊 **Real-time Statistics** - See everything at a glance
- 📈 **Historical Trends** - Track performance over time (coming soon)
- 🎛️ **Centralized Control** - Manage all services from one place
- 🌙 **Beautiful Dark UI** - Matches your Plex aesthetic
- 💾 **Persistent Config** - Set it up once, it just works

---

## 🚀 Quick Start

### For Users

**Get started in 3 steps:**

1. **Run the setup:**
   ```bash
   setup-dev.bat
   ```

2. **Start Totarr:**
   ```bash
   start-simple.bat
   ```

3. **Open your browser:**
   - Navigate to http://localhost:3000
   - Connect your Plex server
   - Add your *arr integrations (optional)
   - Start monitoring!

📖 **Need help?** Check out [QUICK_START.md](QUICK_START.md)

### For Developers

**Want to contribute or customize?**

1. **Clone the repo:**
   ```bash
   git clone <repo-url>
   cd totarr
   ```

2. **Check the docs:**
   - [START_HERE.md](Claude_Docs/START_HERE.md) - Development overview
   - [HANDOFF_SUMMARY.md](Claude_Docs/HANDOFF_SUMMARY.md) - Complete context
   - [README.md](README.md) - Technical details

3. **Start developing:**
   - Backend: FastAPI + Python
   - Frontend: React + TypeScript + Material-UI
   - Database: SQLite (dev) or TimescaleDB (prod)

---

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast Python web framework
- **SQLAlchemy** - Database ORM
- **PlexAPI** - Plex integration
- **TimescaleDB** - Time-series statistics (optional)

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Material-UI** - Beautiful components
- **Zustand** - State management

### Deployment
- **Docker** - Containerized deployment
- **Unraid** - Native support (templates coming)
- **SQLite/PostgreSQL** - Flexible database options

---

## 📸 Screenshots

*(Coming soon - add screenshots of your actual UI here)*

---

## 🗺️ Roadmap

### ✅ Current (v0.3)
- [x] Plex integration
- [x] Library management
- [x] Scan history
- [x] *arr integrations (Radarr, Sonarr, SABnzbd, Prowlarr)
- [x] Real-time statistics dashboard
- [x] Professional configuration system

### 🔄 In Progress
- [ ] TimescaleDB time-series storage
- [ ] Historical statistics & trends
- [ ] Settings page
- [ ] Docker deployment

### 🔮 Future
- [ ] Jellyfin integration
- [ ] Advanced notifications (Discord, Slack, Email)
- [ ] Scheduled tasks & automation
- [ ] Overseerr integration
- [ ] Custom webhooks
- [ ] Multi-user support

---

## 🤝 Contributing

This is an open-source project, and contributions are welcome!

**Ways to contribute:**
- 🐛 Report bugs
- 💡 Suggest features
- 📖 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the project

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Technical overview & installation |
| [QUICK_START.md](QUICK_START.md) | Get up and running fast |
| [DATABASE_SETUP.md](DATABASE_SETUP.md) | Database configuration guide |
| [START_HERE.md](Claude_Docs/START_HERE.md) | Development getting started |
| [HANDOFF_SUMMARY.md](Claude_Docs/HANDOFF_SUMMARY.md) | Complete development context |
| [RENAME_SUMMARY.md](RENAME_SUMMARY.md) | Project rename details |

---

## 💬 Community

- **GitHub Issues** - Bug reports and feature requests
- **Discord** - Coming soon!
- **Reddit** - r/selfhosted, r/PleX

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

---

## 🙏 Acknowledgments

Totarr wouldn't be possible without these amazing projects:

- **Plex** - The media server that started it all
- **Jellyfin** - Open-source media freedom
- **The *arr Community** - Radarr, Sonarr, Prowlarr, Lidarr, Readarr
- **SABnzbd** - The binary newsgrabber
- **FastAPI** - Making Python web APIs a joy
- **React** - The UI library we love
- **Material-UI** - Beautiful components out of the box
- **TimescaleDB** - Time-series data done right

And the entire self-hosting community! 🎉

---

## ⭐ Show Your Support

If you find Totarr useful, please consider:
- ⭐ **Starring** the repository
- 🐛 **Reporting** bugs you find
- 💡 **Sharing** feature ideas
- 📢 **Telling** others about it

---

**Built with ❤️ by the self-hosting community, for the self-hosting community**

*Totarr - Because managing all your *arr apps shouldn't be a chore*

---

## 🔗 Quick Links

- 🌐 **Web UI:** http://localhost:3000
- 🔌 **API:** http://localhost:8000
- 📖 **API Docs:** http://localhost:8000/api/docs
- 🐙 **GitHub:** (add your repo URL)
- 📝 **Changelog:** (coming soon)

---

**Version:** 0.3.0  
**Status:** Active Development  
**Last Updated:** November 8, 2025
