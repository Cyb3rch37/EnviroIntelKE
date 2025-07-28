# EnviroIntel KE - Environmental Cyber Intelligence Platform

🌍 **Environmental cyber intelligence platform for Kenya's environmental protection**

## Features

- **Real-Time Threat Dashboard** - Live environmental threat monitoring across Kenya
- **Predictive Analytics** - AI-powered insights for environmental risks
- **Geospatial Visualization** - Interactive maps showing threat locations
- **Public API** - RESTful endpoints for government and NGO integration
- **Multi-source Intelligence** - Combines satellite data, social media, and sensor networks

## Tech Stack

- **Frontend**: React.js with Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Deployment**: Render (single web service)

## Local Development

### Prerequisites
- Node.js 16+
- Python 3.8+
- MongoDB

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/envirointel-ke.git
   cd envirointel-ke
   ```

2. **Install dependencies**
   ```bash
   npm run install-all
   ```

3. **Set up environment variables**
   ```bash
   # Create backend/.env
   MONGO_URL=mongodb://localhost:27017/envirointel_ke
   
   # Create frontend/.env
   REACT_APP_BACKEND_URL=http://localhost:8001
   ```

4. **Run development servers**
   ```bash
   npm run dev
   ```

## Deployment on Render

### One-Click Deploy
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Manual Deployment

1. **Connect your GitHub repository to Render**
2. **Set environment variables in Render dashboard:**
   - `MONGO_URL`: Your MongoDB connection string
   - `NODE_ENV`: production

3. **Deploy using the included `render.yaml` configuration**

The application will automatically:
- Build the React frontend
- Copy static files to the backend
- Install Python dependencies
- Start the FastAPI server serving both API and frontend

## API Endpoints

- `GET /api/threats` - All environmental threats
- `GET /api/threats/{type}` - Threats by type
- `GET /api/insights` - Predictive insights
- `GET /api/stats` - Dashboard statistics
- `GET /api/alerts/recent` - Recent alerts

## Environment Variables

### Required
- `MONGO_URL` - MongoDB connection string

### Optional
- `NODE_ENV` - Environment (development/production)
- `PORT` - Server port (auto-set by Render)

## Project Structure

```
envirointel-ke/
├── backend/
│   ├── server.py          # FastAPI application
│   ├── requirements.txt   # Python dependencies
│   └── static/           # React build files (auto-generated)
├── frontend/
│   ├── src/              # React source code
│   ├── package.json      # Node.js dependencies
│   └── build/           # React build output
├── render.yaml          # Render deployment config
└── package.json         # Root package file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For questions and support, please open an issue in the GitHub repository.

---

**EnviroIntel KE** - Protecting Kenya's environment through cyber intelligence 🇰🇪