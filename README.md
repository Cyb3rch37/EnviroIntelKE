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
=======
# EnviroIntelKE

[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)](https://numpy.org/)
[![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-0E7C7B?logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Typer](https://img.shields.io/badge/Typer-5A69C7?logo=typer&logoColor=white)](https://typer.tiangolo.com/)
[![npm](https://img.shields.io/badge/npm-CB3837?logo=npm&logoColor=white)](https://www.npmjs.com/)
[![Yarn](https://img.shields.io/badge/Yarn-2C8EBB?logo=yarn&logoColor=white)](https://yarnpkg.com/)
[![Axios](https://img.shields.io/badge/Axios-5A29E4?logo=axios&logoColor=white)](https://axios-http.com/)
[![Autoprefixer](https://img.shields.io/badge/Autoprefixer-DD3735?logo=autoprefixer&logoColor=white)](https://github.com/postcss/autoprefixer)
[![PostCSS](https://img.shields.io/badge/PostCSS-DD3A0A?logo=postcss&logoColor=white)](https://postcss.org/)
[![Markdown](https://img.shields.io/badge/Markdown-000000?logo=markdown&logoColor=white)](https://daringfireball.net/projects/markdown/)
[![ESLint](https://img.shields.io/badge/ESLint-4B32C3?logo=eslint&logoColor=white)](https://eslint.org/)
[![JSON](https://img.shields.io/badge/JSON-5C5C5C?logo=json&logoColor=white)](https://www.json.org/)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

---

## Overview

**EnviroIntelKE** is an advanced environmental threat intelligence platform by [Cyb3rch37](https://github.com/Cyb3rch37) tailored for developers seeking reliable, scalable monitoring solutions. It combines comprehensive backend API testing, structured quality assurance protocols, and a modular frontend architecture to streamline development and deployment.

## Features

- **Full Stack:** Combines Python (FastAPI, Typer, Pydantic, NumPy, pandas) and JavaScript (React, Axios, npm/Yarn, PostCSS, Autoprefixer, ESLint).
- **Modern Frontend:** Built with React for interactive UI.
- **Robust Backend:** FastAPI powers the backend API, with data models using Pydantic.
- **Testing:** Automated tests via Pytest.
- **Data Handling:** Uses pandas and NumPy for data analysis.
- **Linting & Formatting:** Ensured by ESLint and PostCSS plugins.
- **Dependency Management:** Supports npm and Yarn.

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Cyb3rch37/EnviroIntelKE.git
   cd EnviroIntelKE
   ```

2. **Install dependencies:**  
   For backend (Python):
   ```bash
   pip install -r requirements.txt
   ```
   For frontend (JavaScript/React):
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Run the application:**  
   Backend:
   ```bash
   uvicorn main:app --reload
   ```
   Frontend:
   ```bash
   npm start
   # or
   yarn start
   ```

## Contributing

Pull requests, issues, and feature requests are welcome!  
Please refer to the repository's Wiki and Projects tab for additional documentation and planning.

## License

MIT License

Copyright (c) 2025 Cyb3rch37

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Author

Maintained by [Cyb3rch37](https://github.com/Cyb3rch37).

---

[Repository Link](https://github.com/Cyb3rch37/EnviroIntelKE)
