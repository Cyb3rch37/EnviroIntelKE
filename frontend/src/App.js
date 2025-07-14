import React, { useState, useEffect } from 'react';
import './App.css';

const App = () => {
  const [threats, setThreats] = useState([]);
  const [insights, setInsights] = useState([]);
  const [stats, setStats] = useState({});
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedThreatType, setSelectedThreatType] = useState('all');
  const [recentAlerts, setRecentAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

  useEffect(() => {
    fetchData();
    // Set up real-time updates
    const interval = setInterval(fetchRecentAlerts, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [threatsRes, insightsRes, statsRes, alertsRes] = await Promise.all([
        fetch(`${backendUrl}/api/threats`),
        fetch(`${backendUrl}/api/insights`),
        fetch(`${backendUrl}/api/stats`),
        fetch(`${backendUrl}/api/alerts/recent`)
      ]);

      const threatsData = await threatsRes.json();
      const insightsData = await insightsRes.json();
      const statsData = await statsRes.json();
      const alertsData = await alertsRes.json();

      setThreats(threatsData.threats || []);
      setInsights(insightsData.insights || []);
      setStats(statsData);
      setRecentAlerts(alertsData.alerts || []);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchRecentAlerts = async () => {
    try {
      const response = await fetch(`${backendUrl}/api/alerts/recent`);
      const data = await response.json();
      setRecentAlerts(data.alerts || []);
    } catch (error) {
      console.error('Error fetching recent alerts:', error);
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical': return 'bg-red-500';
      case 'high': return 'bg-orange-500';
      case 'medium': return 'bg-yellow-500';
      case 'low': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const getThreatTypeIcon = (type) => {
    switch (type) {
      case 'deforestation': return '🌳';
      case 'pollution': return '🏭';
      case 'illegal_dumping': return '🗑️';
      case 'climate_anomaly': return '🌡️';
      default: return '⚠️';
    }
  };

  const formatDateTime = (dateString) => {
    return new Date(dateString).toLocaleString();
  };

  const filteredThreats = selectedThreatType === 'all' 
    ? threats 
    : threats.filter(threat => threat.type === selectedThreatType);

  const StatsCard = ({ title, value, icon, color }) => (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
        <div className={`p-3 rounded-full ${color}`}>
          <span className="text-white text-xl">{icon}</span>
        </div>
      </div>
    </div>
  );

  const ThreatMarker = ({ threat }) => (
    <div className="bg-white p-4 rounded-lg shadow-md mb-4 border-l-4 border-blue-500">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center">
          <span className="text-xl mr-2">{getThreatTypeIcon(threat.type)}</span>
          <h3 className="text-lg font-semibold text-gray-900">{threat.title}</h3>
        </div>
        <div className="flex items-center space-x-2">
          <span className={`px-2 py-1 text-xs font-medium text-white rounded-full ${getSeverityColor(threat.severity)}`}>
            {threat.severity.toUpperCase()}
          </span>
          <span className="text-sm text-gray-500">{Math.round(threat.confidence * 100)}%</span>
        </div>
      </div>
      <p className="text-gray-600 mb-2">{threat.description}</p>
      <div className="flex items-center justify-between text-sm text-gray-500">
        <span>📍 {threat.location.name}</span>
        <span>🕒 {formatDateTime(threat.timestamp)}</span>
        <span>📡 {threat.source}</span>
      </div>
    </div>
  );

  const InsightCard = ({ insight }) => (
    <div className="bg-white p-6 rounded-lg shadow-md mb-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold text-gray-900">{insight.title}</h3>
        <span className={`px-3 py-1 text-sm font-medium rounded-full ${
          insight.risk_level === 'critical' ? 'bg-red-100 text-red-800' :
          insight.risk_level === 'high' ? 'bg-orange-100 text-orange-800' :
          'bg-yellow-100 text-yellow-800'
        }`}>
          {insight.risk_level.toUpperCase()}
        </span>
      </div>
      <p className="text-gray-600 mb-3">{insight.description}</p>
      <div className="flex items-center justify-between text-sm text-gray-500">
        <span>📊 {Math.round(insight.probability * 100)}% probability</span>
        <span>⏱️ {insight.timeframe}</span>
      </div>
      <div className="mt-2">
        <span className="text-sm text-gray-500">Affected areas: {insight.affected_areas.join(', ')}</span>
      </div>
    </div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
          <p className="mt-4 text-lg text-gray-600">Loading EnviroIntel KE...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <span className="text-2xl font-bold text-green-600">🌍 EnviroIntel KE</span>
              </div>
              <nav className="ml-10 flex space-x-8">
                <button
                  onClick={() => setActiveTab('dashboard')}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    activeTab === 'dashboard' 
                      ? 'text-blue-600 bg-blue-50' 
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Dashboard
                </button>
                <button
                  onClick={() => setActiveTab('threats')}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    activeTab === 'threats' 
                      ? 'text-blue-600 bg-blue-50' 
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Threats
                </button>
                <button
                  onClick={() => setActiveTab('insights')}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    activeTab === 'insights' 
                      ? 'text-blue-600 bg-blue-50' 
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  Predictive Insights
                </button>
                <button
                  onClick={() => setActiveTab('api')}
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    activeTab === 'api' 
                      ? 'text-blue-600 bg-blue-50' 
                      : 'text-gray-500 hover:text-gray-700'
                  }`}
                >
                  API
                </button>
              </nav>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">
                Last updated: {stats.last_updated ? new Date(stats.last_updated).toLocaleTimeString() : 'Loading...'}
              </span>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span className="text-sm text-green-600">Live</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'dashboard' && (
          <div className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <StatsCard 
                title="Total Threats" 
                value={stats.total_threats || 0} 
                icon="⚠️" 
                color="bg-red-500" 
              />
              <StatsCard 
                title="Active Threats" 
                value={stats.active_threats || 0} 
                icon="🔥" 
                color="bg-orange-500" 
              />
              <StatsCard 
                title="Critical Alerts" 
                value={stats.critical_threats || 0} 
                icon="🚨" 
                color="bg-red-600" 
              />
              <StatsCard 
                title="Resolved" 
                value={stats.resolved_threats || 0} 
                icon="✅" 
                color="bg-green-500" 
              />
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Map Placeholder */}
              <div className="lg:col-span-2 bg-white p-6 rounded-lg shadow-md">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Kenya Environmental Threat Map</h2>
                <div className="h-96 bg-green-50 rounded-lg flex items-center justify-center relative overflow-hidden">
                  <div className="absolute inset-0 bg-gradient-to-br from-green-100 to-blue-100"></div>
                  <div className="relative z-10 text-center">
                    <div className="text-4xl mb-4">🗺️</div>
                    <p className="text-lg font-medium text-gray-700">Interactive Map of Kenya</p>
                    <p className="text-sm text-gray-500 mt-2">Real-time environmental threat visualization</p>
                    <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
                      <div className="flex items-center justify-center space-x-2">
                        <span className="w-3 h-3 bg-red-500 rounded-full"></span>
                        <span>Critical Threats</span>
                      </div>
                      <div className="flex items-center justify-center space-x-2">
                        <span className="w-3 h-3 bg-yellow-500 rounded-full"></span>
                        <span>Moderate Risks</span>
                      </div>
                      <div className="flex items-center justify-center space-x-2">
                        <span className="w-3 h-3 bg-green-500 rounded-full"></span>
                        <span>Low Impact</span>
                      </div>
                      <div className="flex items-center justify-center space-x-2">
                        <span className="w-3 h-3 bg-blue-500 rounded-full"></span>
                        <span>Protected Areas</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Recent Alerts */}
              <div className="bg-white p-6 rounded-lg shadow-md">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Alerts</h2>
                <div className="space-y-3 max-h-96 overflow-y-auto">
                  {recentAlerts.slice(0, 8).map((alert, index) => (
                    <div key={index} className="border-l-4 border-blue-500 pl-4 py-2">
                      <div className="flex items-center space-x-2">
                        <span>{getThreatTypeIcon(alert.type)}</span>
                        <span className="text-sm font-medium text-gray-900">{alert.title}</span>
                      </div>
                      <p className="text-xs text-gray-500 mt-1">{alert.location.name}</p>
                      <p className="text-xs text-gray-400">{formatDateTime(alert.timestamp)}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Threat Distribution */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Threat Distribution</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {stats.threat_distribution && Object.entries(stats.threat_distribution).map(([type, count]) => (
                  <div key={type} className="text-center p-4 bg-gray-50 rounded-lg">
                    <div className="text-2xl mb-2">{getThreatTypeIcon(type)}</div>
                    <div className="text-lg font-bold text-gray-900">{count}</div>
                    <div className="text-sm text-gray-500 capitalize">{type.replace('_', ' ')}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'threats' && (
          <div className="space-y-6">
            {/* Threat Filters */}
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Environmental Threats</h2>
              <div className="flex flex-wrap gap-2 mb-4">
                <button
                  onClick={() => setSelectedThreatType('all')}
                  className={`px-4 py-2 rounded-full text-sm font-medium ${
                    selectedThreatType === 'all' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  All Threats ({threats.length})
                </button>
                <button
                  onClick={() => setSelectedThreatType('deforestation')}
                  className={`px-4 py-2 rounded-full text-sm font-medium ${
                    selectedThreatType === 'deforestation' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  🌳 Deforestation
                </button>
                <button
                  onClick={() => setSelectedThreatType('pollution')}
                  className={`px-4 py-2 rounded-full text-sm font-medium ${
                    selectedThreatType === 'pollution' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  🏭 Pollution
                </button>
                <button
                  onClick={() => setSelectedThreatType('illegal_dumping')}
                  className={`px-4 py-2 rounded-full text-sm font-medium ${
                    selectedThreatType === 'illegal_dumping' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  🗑️ Illegal Dumping
                </button>
                <button
                  onClick={() => setSelectedThreatType('climate_anomaly')}
                  className={`px-4 py-2 rounded-full text-sm font-medium ${
                    selectedThreatType === 'climate_anomaly' 
                      ? 'bg-blue-600 text-white' 
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  🌡️ Climate Anomaly
                </button>
              </div>
            </div>

            {/* Threats List */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {filteredThreats.map((threat) => (
                <ThreatMarker key={threat.id} threat={threat} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'insights' && (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Predictive Environmental Insights</h2>
              <p className="text-gray-600 mb-6">
                AI-powered predictions and early warning systems for environmental threats across Kenya
              </p>
            </div>

            <div className="space-y-6">
              {insights.map((insight) => (
                <InsightCard key={insight.id} insight={insight} />
              ))}
            </div>
          </div>
        )}

        {activeTab === 'api' && (
          <div className="space-y-6">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Public API Documentation</h2>
              <p className="text-gray-600 mb-6">
                RESTful API endpoints for accessing environmental threat data and predictive insights
              </p>
              
              <div className="space-y-4">
                <div className="border-l-4 border-blue-500 pl-4">
                  <h3 className="font-medium text-gray-900">GET /api/threats</h3>
                  <p className="text-sm text-gray-600">Retrieve all environmental threats</p>
                </div>
                
                <div className="border-l-4 border-green-500 pl-4">
                  <h3 className="font-medium text-gray-900">GET /api/threats/{type}</h3>
                  <p className="text-sm text-gray-600">Get threats by type (deforestation, pollution, etc.)</p>
                </div>
                
                <div className="border-l-4 border-purple-500 pl-4">
                  <h3 className="font-medium text-gray-900">GET /api/insights</h3>
                  <p className="text-sm text-gray-600">Access predictive environmental insights</p>
                </div>
                
                <div className="border-l-4 border-orange-500 pl-4">
                  <h3 className="font-medium text-gray-900">GET /api/stats</h3>
                  <p className="text-sm text-gray-600">Dashboard statistics and metrics</p>
                </div>
                
                <div className="border-l-4 border-red-500 pl-4">
                  <h3 className="font-medium text-gray-900">GET /api/alerts/recent</h3>
                  <p className="text-sm text-gray-600">Latest environmental alerts</p>
                </div>
              </div>
              
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <h4 className="font-medium text-gray-900 mb-2">API Base URL:</h4>
                <code className="text-sm text-blue-600">{backendUrl}</code>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default App;