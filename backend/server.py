from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List
import os
import uuid
from datetime import datetime, timedelta
import random
from pathlib import Path

app = FastAPI(
    title="EnviroIntel KE API",
    description="Environmental Cyber Intelligence Platform for Kenya",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')
client = MongoClient(mongo_url)
db = client.envirointel_ke

# Configure static files
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

print(f"🔍 Static directory: {static_dir}")
if static_dir.exists():
    print("✅ Static files directory found")
    print("📂 Directory contents:")
    for f in static_dir.glob("*"):
        print(f" - {f.name}{'/' if f.is_dir() else ''}")
else:
    print("⚠️ Static files directory not found!")

# Pydantic models
class ThreatAlert(BaseModel):
    id: str
    type: str
    title: str
    description: str
    location: dict
    severity: str
    confidence: float
    timestamp: datetime
    source: str
    status: str

class PredictiveInsight(BaseModel):
    id: str
    type: str
    title: str
    description: str
    risk_level: str
    probability: float
    timeframe: str
    affected_areas: List[str]
    timestamp: datetime

# Mock data generation
def generate_mock_threats():
    kenya_locations = [
        {"lat": -1.2921, "lng": 36.8219, "name": "Nairobi"},
        {"lat": -4.0435, "lng": 39.6682, "name": "Mombasa"},
        {"lat": 0.5143, "lng": 35.2697, "name": "Kakamega Forest"},
        {"lat": -0.0917, "lng": 34.7680, "name": "Kisumu"},
        {"lat": 0.1169, "lng": 37.9083, "name": "Samburu"},
        {"lat": -2.1742, "lng": 40.1167, "name": "Tsavo East"},
        {"lat": -1.4037, "lng": 36.9630, "name": "Naivasha"},
        {"lat": 2.7308, "lng": 39.2606, "name": "Lamu"},
        {"lat": -0.8833, "lng": 36.0667, "name": "Nakuru"},
        {"lat": 1.9403, "lng": 37.0983, "name": "Turkana"}
    ]
    
    threat_types = {
        "deforestation": {
            "titles": ["Illegal Logging Detected", "Forest Canopy Loss", "Charcoal Production Site"],
            "descriptions": ["Satellite imagery shows significant tree loss", "Unusual forest clearing activity detected", "Illegal charcoal production identified"]
        },
        "pollution": {
            "titles": ["Air Quality Alert", "Water Contamination", "Industrial Pollution"],
            "descriptions": ["PM2.5 levels exceed safe limits", "Chemical contamination detected", "Industrial waste discharge identified"]
        },
        "illegal_dumping": {
            "titles": ["Illegal Waste Dump", "Plastic Pollution", "Chemical Waste Site"],
            "descriptions": ["Large waste accumulation detected", "Plastic debris concentration", "Hazardous waste disposal identified"]
        },
        "climate_anomaly": {
            "titles": ["Drought Risk", "Flood Warning", "Temperature Anomaly"],
            "descriptions": ["Severe drought conditions developing", "Flash flood risk elevated", "Unusual temperature patterns detected"]
        }
    }
    
    threats = []
    for _ in range(25):
        threat_type = random.choice(list(threat_types.keys()))
        location = random.choice(kenya_locations)
        threat_data = threat_types[threat_type]
        
        threats.append(ThreatAlert(
            id=str(uuid.uuid4()),
            type=threat_type,
            title=random.choice(threat_data["titles"]),
            description=random.choice(threat_data["descriptions"]),
            location=location,
            severity=random.choice(["low", "medium", "high", "critical"]),
            confidence=round(random.uniform(0.6, 0.95), 2),
            timestamp=datetime.now() - timedelta(hours=random.randint(0, 48)),
            source=random.choice(["Satellite", "Social Media", "Citizen Report", "Sensor Network"]),
            status=random.choice(["active", "investigating", "resolved"])
        ))
    
    return threats

def generate_mock_insights():
    return [
        PredictiveInsight(
            id=str(uuid.uuid4()),
            type="drought_prediction",
            title="Drought Risk - Northern Kenya",
            description="Climate models indicate 78% probability of severe drought conditions in Turkana and Marsabit counties within next 3 months",
            risk_level="high",
            probability=0.78,
            timeframe="3 months",
            affected_areas=["Turkana", "Marsabit", "Wajir"],
            timestamp=datetime.now()
        ),
        PredictiveInsight(
            id=str(uuid.uuid4()),
            type="deforestation_prediction",
            title="Forest Loss Projection - Kakamega",
            description="ML models predict 12% increase in illegal logging activity during dry season based on historical patterns",
            risk_level="medium",
            probability=0.65,
            timeframe="2 months",
            affected_areas=["Kakamega", "Nandi", "Vihiga"],
            timestamp=datetime.now()
        ),
        PredictiveInsight(
            id=str(uuid.uuid4()),
            type="pollution_prediction",
            title="Air Quality Deterioration - Nairobi",
            description="Traffic and industrial patterns suggest 45% increase in PM2.5 levels during upcoming industrial season",
            risk_level="medium",
            probability=0.72,
            timeframe="1 month",
            affected_areas=["Nairobi", "Kiambu", "Machakos"],
            timestamp=datetime.now()
        ),
        PredictiveInsight(
            id=str(uuid.uuid4()),
            type="flood_prediction",
            title="Flood Risk - Coastal Region",
            description="Monsoon patterns and soil moisture data indicate 85% probability of flooding in coastal areas",
            risk_level="critical",
            probability=0.85,
            timeframe="1 month",
            affected_areas=["Mombasa", "Kilifi", "Kwale"],
            timestamp=datetime.now()
        )
    ]

# API Routes
@app.get("/")
async def root():
    return FileResponse(static_dir / 'index.html')

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/threats")
async def get_threats():
    return {"threats": [threat.dict() for threat in generate_mock_threats()]}

@app.get("/api/threats/{threat_type}")
async def get_threats_by_type(threat_type: str):
    threats = [t for t in generate_mock_threats() if t.type == threat_type]
    return {"threats": [t.dict() for t in threats]}

@app.get("/api/insights")
async def get_predictive_insights():
    return {"insights": [insight.dict() for insight in generate_mock_insights()]}

@app.get("/api/stats")
async def get_dashboard_stats():
    threats = generate_mock_threats()
    return {
        "total_threats": len(threats),
        "active_threats": len([t for t in threats if t.status == "active"]),
        "critical_threats": len([t for t in threats if t.severity == "critical"]),
        "resolved_threats": len([t for t in threats if t.status == "resolved"]),
        "threat_distribution": {t: sum(1 for th in threats if th.type == t) for t in set(th.type for th in threats)},
        "severity_distribution": {s: sum(1 for th in threats if th.severity == s) for s in set(th.severity for th in threats)},
        "last_updated": datetime.now().isoformat()
    }

@app.post("/api/threats/{threat_id}/status")
async def update_threat_status(threat_id: str, status: str):
    return {"message": f"Threat {threat_id} status updated to {status}"}

@app.get("/api/alerts/recent")
async def get_recent_alerts():
    threats = sorted(generate_mock_threats(), key=lambda x: x.timestamp, reverse=True)[:10]
    return {"alerts": [t.dict() for t in threats]}

# Static file routes
@app.get("/favicon.ico")
async def favicon():
    return FileResponse(static_dir / "favicon.ico")

@app.get("/manifest.json")
async def manifest():
    return FileResponse(static_dir / "manifest.json")

# Serve React app for all other routes
@app.get("/{path:path}")
async def serve_react_app(path: str):
    # Check if it's a static file request
    if path.startswith("static/"):
        file_path = static_dir / path
        if file_path.exists():
            return FileResponse(file_path)
        raise HTTPException(status_code=404)
    
    # Serve index.html for all other routes
    return FileResponse(static_dir / 'index.html')

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)  # Explicit host binding
