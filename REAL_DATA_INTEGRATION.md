# Real Data Integration - EnviroIntel KE

## Overview
The EnviroIntel KE API has been enhanced with real-time environmental data integration from external APIs. This provides more accurate and current environmental threat detection for Kenya.

## New Features

### 1. Real Weather Data Integration
- **Source**: OpenWeatherMap API
- **Coverage**: 8 major Kenyan cities (Nairobi, Mombasa, Kisumu, Nakuru, Eldoret, Thika, Malindi, Nyeri)
- **Data Points**: Temperature, humidity, pressure, wind speed, weather conditions, visibility
- **Endpoint**: `GET /api/weather`

### 2. Real Air Quality Data Integration
- **Source**: OpenAQ API
- **Coverage**: Available monitoring stations in Kenya
- **Data Points**: PM2.5, PM10, NO2, SO2, calculated AQI
- **Endpoint**: `GET /api/air-quality`

### 3. Enhanced Threat Detection
The system now generates real environmental threats based on:

#### Climate Anomaly Threats
- **Extreme Heat**: Temperature > 35°C (High severity if > 40°C)
- **Unusual Cold**: Temperature < 10°C (unusual for Kenya)
- **Strong Winds**: Wind speed > 15 m/s
- **Poor Visibility**: < 2km (potential air quality issues)

#### Pollution Threats
- **High PM2.5**: > 35 µg/m³ (WHO guideline: 15 µg/m³)
- **High PM10**: > 50 µg/m³ (WHO guideline: 45 µg/m³)
- **High NO2**: > 40 µg/m³ (traffic/industrial pollution indicator)

### 4. Updated API Endpoints

#### Enhanced Threats Endpoint
```
GET /api/threats
```
Now returns:
- Real climate threats from weather data
- Real pollution threats from air quality data
- Mock threats for deforestation and illegal dumping
- Metadata: `total`, `real_data_threats`, `mock_threats`

#### Enhanced Stats Endpoint
```
GET /api/stats
```
Now includes:
- `real_data_sources`: Array of external data sources used
- Updated threat distributions including real data

## Configuration

### Environment Variables
Create a `.env` file in the `/app/backend/` directory:

```env
# OpenWeatherMap API Key (required for weather data)
OPENWEATHER_API_KEY=your_api_key_here

# MongoDB Connection
MONGO_URL=mongodb://localhost:27017/

# Server Configuration
PORT=8001
```

### Getting API Keys

#### OpenWeatherMap API Key
1. Visit https://openweathermap.org/api
2. Sign up for a free account
3. Generate an API key
4. Add it to your `.env` file

## Data Flow

1. **Weather Data**: Fetched from OpenWeatherMap every API call
2. **Air Quality Data**: Fetched from OpenAQ every API call
3. **Threat Generation**: Real-time analysis of fetched data against thresholds
4. **Fallback**: If external APIs fail, system falls back to mock data

## Error Handling

- **API Failures**: Graceful fallback to mock data
- **Network Timeouts**: 10-15 second timeouts with error logging
- **Missing API Keys**: Weather data disabled, air quality still attempted

## Performance Considerations

- **Caching**: Consider implementing caching for external API calls
- **Rate Limits**: OpenWeatherMap free tier: 1000 calls/day
- **Async Processing**: All external API calls are asynchronous

## Future Enhancements

1. **Satellite Data Integration**: For deforestation detection
2. **Social Media Monitoring**: For citizen reports
3. **Sensor Network Integration**: Direct sensor data feeds
4. **Predictive Analytics**: ML models for threat prediction
5. **Data Caching**: Redis/Memcached for improved performance

## Testing

Test the new endpoints:

```bash
# Health check
curl http://localhost:8001/health

# Weather data
curl http://localhost:8001/api/weather

# Air quality data
curl http://localhost:8001/api/air-quality

# Enhanced threats
curl http://localhost:8001/api/threats

# Enhanced stats
curl http://localhost:8001/api/stats
```

## Dependencies Added

- `httpx`: Async HTTP client for external API calls
- `python-dotenv`: Environment variable management (already present)

## Monitoring Locations

The system monitors these Kenyan locations:
- Nairobi (-1.2921, 36.8219)
- Mombasa (-4.0435, 39.6682)
- Kisumu (-0.0917, 34.7680)
- Nakuru (-0.3031, 36.0800)
- Eldoret (0.5143, 35.2697)
- Thika (-1.0332, 37.0689)
- Malindi (-3.2175, 40.1169)
- Nyeri (-0.4167, 36.9500)