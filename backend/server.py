from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Optional
import os
import uuid
from datetime import datetime, timedelta
import random
from pathlib import Path
import httpx
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()

app = FastAPI(title="EnviroIntel KE API")

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

# API Keys
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')

# Serve React static files (for production deployment)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Pydantic models
class ThreatAlert(BaseModel):
    id: str
    type: str  # deforestation, pollution, illegal_dumping, climate_anomaly
    title: str
    description: str
    location: dict  # {lat, lng, name}
    severity: str  # low, medium, high, critical
    confidence: float
    timestamp: datetime
    source: str
    status: str  # active, resolved, investigating

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

class WeatherData(BaseModel):
    location: str
    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    weather_condition: str
    visibility: float
    timestamp: datetime

class AirQualityData(BaseModel):
    location: str
    pm25: Optional[float]
    pm10: Optional[float]
    no2: Optional[float]
    so2: Optional[float]
    aqi: Optional[int]
    timestamp: datetime

# Kenya locations for environmental monitoring
KENYA_LOCATIONS = [
    {"name": "Nairobi", "lat": -1.2921, "lng": 36.8219},
    {"name": "Mombasa", "lat": -4.0435, "lng": 39.6682},
    {"name": "Kisumu", "lat": -0.0917, "lng": 34.7680},
    {"name": "Nakuru", "lat": -0.3031, "lng": 36.0800},
    {"name": "Eldoret", "lat": 0.5143, "lng": 35.2697},
    {"name": "Thika", "lat": -1.0332, "lng": 37.0689},
    {"name": "Malindi", "lat": -3.2175, "lng": 40.1169},
    {"name": "Nyeri", "lat": -0.4167, "lng": 36.9500}
]

# Real weather data integration
async def get_real_weather_data():
    """Fetch real weather data from OpenWeatherMap for Kenya locations"""
    if not OPENWEATHER_API_KEY:
        return []
    
    weather_data = []
    async with httpx.AsyncClient() as http_client:
        for location in KENYA_LOCATIONS:
            try:
                response = await http_client.get(
                    f"https://api.openweathermap.org/data/2.5/weather",
                    params={
                        "lat": location["lat"],
                        "lon": location["lng"],
                        "appid": OPENWEATHER_API_KEY,
                        "units": "metric"
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    weather_data.append({
                        "location": location["name"],
                        "temperature": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "pressure": data["main"]["pressure"],
                        "wind_speed": data["wind"].get("speed", 0),
                        "weather_condition": data["weather"][0]["main"],
                        "visibility": data.get("visibility", 10000) / 1000,  # Convert to km
                        "timestamp": datetime.now()
                    })
                    
            except Exception as e:
                print(f"Error fetching weather data for {location['name']}: {e}")
                continue
                
    return weather_data

# Real air quality data integration
async def get_real_air_quality_data():
    """Fetch real air quality data from OpenAQ for Kenya"""
    air_quality_data = []
    
    async with httpx.AsyncClient() as http_client:
        try:
            # Fetch latest air quality measurements for Kenya
            response = await http_client.get(
                "https://api.openaq.org/v2/latest",
                params={
                    "country": "KE",  # Kenya ISO code
                    "parameter": "pm25,pm10,no2,so2",
                    "limit": 100
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                for result in data.get("results", []):
                    location_name = result.get("location", "Unknown")
                    measurements = {}
                    aqi_value = None
                    
                    # Process measurements
                    for measurement in result.get("measurements", []):
                        param = measurement.get("parameter")
                        value = measurement.get("value")
                        
                        if param == "pm25":
                            measurements["pm25"] = value
                            # Simple AQI calculation for PM2.5
                            if value <= 12:
                                aqi_value = min(50, int((value/12) * 50))
                            elif value <= 35.4:
                                aqi_value = int(50 + ((value-12)/(35.4-12)) * 50)
                            elif value <= 55.4:
                                aqi_value = int(100 + ((value-35.4)/(55.4-35.4)) * 50)
                            else:
                                aqi_value = min(300, int(150 + ((value-55.4)/100) * 150))
                        elif param == "pm10":
                            measurements["pm10"] = value
                        elif param == "no2":
                            measurements["no2"] = value
                        elif param == "so2":
                            measurements["so2"] = value
                    
                    air_quality_data.append({
                        "location": location_name,
                        "pm25": measurements.get("pm25"),
                        "pm10": measurements.get("pm10"),
                        "no2": measurements.get("no2"),
                        "so2": measurements.get("so2"),
                        "aqi": aqi_value,
                        "timestamp": datetime.now()
                    })
                    
        except Exception as e:
            print(f"Error fetching air quality data: {e}")
            
    return air_quality_data

# Generate climate anomaly threats from real weather data
async def generate_climate_threats_from_real_data():
    """Generate climate threat alerts based on real weather data"""
    weather_data = await get_real_weather_data()
    climate_threats = []
    
    for weather in weather_data:
        threats = []
        
        # Temperature anomalies
        if weather["temperature"] > 35:  # Very hot
            threats.append({
                "type": "climate_anomaly",
                "title": f"Extreme Heat Warning - {weather['location']}",
                "description": f"Temperature reached {weather['temperature']:.1f}°C, exceeding safe limits",
                "severity": "high" if weather["temperature"] > 40 else "medium"
            })
        elif weather["temperature"] < 10:  # Unusually cold for Kenya
            threats.append({
                "type": "climate_anomaly", 
                "title": f"Unusual Cold Conditions - {weather['location']}",
                "description": f"Temperature dropped to {weather['temperature']:.1f}°C, below normal range",
                "severity": "medium"
            })
            
        # Low visibility (potential air pollution or weather issues)
        if weather["visibility"] < 2:
            threats.append({
                "type": "pollution",
                "title": f"Poor Visibility Alert - {weather['location']}",
                "description": f"Visibility reduced to {weather['visibility']:.1f}km, possible air quality issues",
                "severity": "medium"
            })
            
        # High wind speeds
        if weather["wind_speed"] > 15:  # Strong winds
            threats.append({
                "type": "climate_anomaly",
                "title": f"Strong Wind Alert - {weather['location']}",
                "description": f"Wind speeds reaching {weather['wind_speed']:.1f} m/s, may affect outdoor activities",
                "severity": "low"
            })
        
        for threat in threats:
            climate_threats.append(ThreatAlert(
                id=str(uuid.uuid4()),
                type=threat["type"],
                title=threat["title"],
                description=threat["description"],
                location={"lat": next(loc["lat"] for loc in KENYA_LOCATIONS if loc["name"] == weather["location"]),
                         "lng": next(loc["lng"] for loc in KENYA_LOCATIONS if loc["name"] == weather["location"]),
                         "name": weather["location"]},
                severity=threat["severity"],
                confidence=0.85,
                timestamp=datetime.now(),
                source="Weather Station",
                status="active"
            ))
            
    return climate_threats

# Generate pollution threats from real air quality data
async def generate_pollution_threats_from_real_data():
    """Generate pollution threat alerts based on real air quality data"""
    air_quality_data = await get_real_air_quality_data()
    pollution_threats = []
    
    for aq_data in air_quality_data:
        threats = []
        
        # PM2.5 alerts
        if aq_data["pm25"] and aq_data["pm25"] > 35:  # WHO guideline exceeded
            severity = "critical" if aq_data["pm25"] > 75 else "high"
            threats.append({
                "title": f"High PM2.5 Levels - {aq_data['location']}",
                "description": f"PM2.5 concentration at {aq_data['pm25']:.1f} µg/m³, exceeding WHO guidelines (15 µg/m³)",
                "severity": severity
            })
            
        # PM10 alerts  
        if aq_data["pm10"] and aq_data["pm10"] > 50:  # WHO guideline exceeded
            severity = "high" if aq_data["pm10"] > 100 else "medium"
            threats.append({
                "title": f"High PM10 Levels - {aq_data['location']}",
                "description": f"PM10 concentration at {aq_data['pm10']:.1f} µg/m³, exceeding WHO guidelines (45 µg/m³)",
                "severity": severity
            })
            
        # NO2 alerts
        if aq_data["no2"] and aq_data["no2"] > 40:  # WHO guideline exceeded
            threats.append({
                "title": f"High NO2 Levels - {aq_data['location']}",
                "description": f"NO2 concentration at {aq_data['no2']:.1f} µg/m³, indicating traffic/industrial pollution",
                "severity": "medium"
            })
        
        for threat in threats:
            # Find location coordinates
            location_coords = {"lat": -1.2921, "lng": 36.8219, "name": aq_data["location"]}  # Default to Nairobi
            for loc in KENYA_LOCATIONS:
                if loc["name"].lower() in aq_data["location"].lower():
                    location_coords = {"lat": loc["lat"], "lng": loc["lng"], "name": aq_data["location"]}
                    break
                    
            pollution_threats.append(ThreatAlert(
                id=str(uuid.uuid4()),
                type="pollution",
                title=threat["title"],
                description=threat["description"],
                location=location_coords,
                severity=threat["severity"],
                confidence=0.92,
                timestamp=datetime.now(),
                source="Air Quality Monitor",
                status="active"
            ))
            
    return pollution_threats

# Mock data generation (fallback)
def generate_mock_threats():
    """Generate mock environmental threats across Kenya (fallback when APIs are unavailable)"""
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
        "illegal_dumping": {
            "titles": ["Illegal Waste Dump", "Plastic Pollution", "Chemical Waste Site"],
            "descriptions": ["Large waste accumulation detected", "Plastic debris concentration", "Hazardous waste disposal identified"]
        }
    }
    
    threats = []
    for i in range(12):  # Reduced to make room for real data
        threat_type = random.choice(list(threat_types.keys()))
        location = random.choice(kenya_locations)
        threat_data = threat_types[threat_type]
        
        threat = ThreatAlert(
            id=str(uuid.uuid4()),
            type=threat_type,
            title=random.choice(threat_data["titles"]),
            description=random.choice(threat_data["descriptions"]),
            location=location,
            severity=random.choice(["low", "medium", "high"]),
            confidence=round(random.uniform(0.6, 0.85), 2),
            timestamp=datetime.now() - timedelta(hours=random.randint(0, 48)),
            source=random.choice(["Satellite", "Citizen Report"]),
            status=random.choice(["active", "investigating", "resolved"])
        )
        threats.append(threat)
    
    return threats

def generate_mock_insights():
    """Generate mock predictive insights"""
    insights = [
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
        )
    ]
    return insights

# API Routes
@app.get("/")
async def root():
    index_file = static_dir / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "EnviroIntel KE API - Environmental Cyber Intelligence Platform"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/weather")
async def get_weather_data():
    """Get real-time weather data for Kenya"""
    try:
        weather_data = await get_real_weather_data()
        return {"weather": weather_data, "source": "OpenWeatherMap", "count": len(weather_data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching weather data: {str(e)}")

@app.get("/api/air-quality")
async def get_air_quality_data():
    """Get real-time air quality data for Kenya"""
    try:
        air_quality_data = await get_real_air_quality_data()
        return {"air_quality": air_quality_data, "source": "OpenAQ", "count": len(air_quality_data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching air quality data: {str(e)}")

@app.get("/api/threats")
async def get_threats():
    """Get all environmental threats (combination of real and mock data)"""
    try:
        # Get real climate threats from weather data
        climate_threats = await generate_climate_threats_from_real_data()
        
        # Get real pollution threats from air quality data  
        pollution_threats = await generate_pollution_threats_from_real_data()
        
        # Get mock threats for deforestation and illegal dumping
        mock_threats = generate_mock_threats()
        
        # Combine all threats
        all_threats = climate_threats + pollution_threats + mock_threats
        
        return {
            "threats": [threat.dict() for threat in all_threats],
            "total": len(all_threats),
            "real_data_threats": len(climate_threats) + len(pollution_threats),
            "mock_threats": len(mock_threats)
        }
    except Exception as e:
        # Fallback to mock data if APIs fail
        print(f"Error generating real threats, falling back to mock data: {e}")
        mock_threats = generate_mock_threats()
        return {"threats": [threat.dict() for threat in mock_threats]}

@app.get("/api/threats/{threat_type}")
async def get_threats_by_type(threat_type: str):
    """Get threats by type"""
    threats_data = await get_threats()
    threats = [ThreatAlert(**threat) for threat in threats_data["threats"]]
    filtered_threats = [threat for threat in threats if threat.type == threat_type]
    return {"threats": [threat.dict() for threat in filtered_threats]}

@app.get("/api/insights")
async def get_predictive_insights():
    """Get predictive insights"""
    insights = generate_mock_insights()
    return {"insights": [insight.dict() for insight in insights]}

@app.get("/api/stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    threats_data = await get_threats()
    threats = [ThreatAlert(**threat) for threat in threats_data["threats"]]
    
    # Calculate statistics
    total_threats = len(threats)
    active_threats = len([t for t in threats if t.status == "active"])
    critical_threats = len([t for t in threats if t.severity == "critical"])
    
    # Threat distribution
    threat_distribution = {}
    for threat in threats:
        threat_distribution[threat.type] = threat_distribution.get(threat.type, 0) + 1
    
    # Severity distribution
    severity_distribution = {}
    for threat in threats:
        severity_distribution[threat.severity] = severity_distribution.get(threat.severity, 0) + 1
    
    return {
        "total_threats": total_threats,
        "active_threats": active_threats,
        "critical_threats": critical_threats,
        "resolved_threats": len([t for t in threats if t.status == "resolved"]),
        "threat_distribution": threat_distribution,
        "severity_distribution": severity_distribution,
        "real_data_sources": ["OpenWeatherMap", "OpenAQ"],
        "last_updated": datetime.now().isoformat()
    }

@app.post("/api/threats/{threat_id}/status")
async def update_threat_status(threat_id: str, status: str):
    """Update threat status"""
    # In a real implementation, this would update the database
    return {"message": f"Threat {threat_id} status updated to {status}"}

@app.get("/api/alerts/recent")
async def get_recent_alerts():
    """Get recent alerts for real-time feed"""
    threats_data = await get_threats()
    threats = [ThreatAlert(**threat) for threat in threats_data["threats"]]
    recent_threats = sorted(threats, key=lambda x: x.timestamp, reverse=True)[:10]
    return {"alerts": [threat.dict() for threat in recent_threats]}

# Serve React app for all non-API routes (for production deployment)
@app.get("/{catchall:path}")
async def serve_react_app(catchall: str):
    # Don't serve React app for API routes
    if catchall.startswith("api/") or catchall.startswith("docs") or catchall.startswith("redoc"):
        raise HTTPException(status_code=404, detail="Not found")
    
    # Check if static directory exists (production mode)
    if static_dir.exists():
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
    
    # In development mode, API-only
    raise HTTPException(status_code=404, detail="Not found")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
