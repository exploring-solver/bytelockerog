import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent } from '@mui/material';
import { Bell, Users, AlertTriangle, Camera } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const Dashboard = () => {
  const [stats, setStats] = useState({
    peopleCount: 0,
    alerts: [],
    crowdDensity: [],
    violations: []
  });
  const [videoFeed, setVideoFeed] = useState(null);
  const wsRef = useRef(null);
  const [error, setError] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    const connectWebSocket = () => {
      wsRef.current = new WebSocket('ws://localhost:8000/ws/metrics');

      wsRef.current.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
        setError(null);
      };

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.error) {
            console.error('Server error:', data.error);
            setError(data.error);
          } else {
            setStats(prevStats => ({
              ...prevStats,
              ...data
            }));
            setError(null);
          }
        } catch (e) {
          console.error('Error parsing WebSocket message:', e);
          setError('Error parsing server data');
        }
      };

      wsRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        setError('WebSocket connection error');
        setIsConnected(false);
      };

      wsRef.current.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);
        // Attempt to reconnect after 5 seconds
        setTimeout(connectWebSocket, 5000);
      };
    };

    connectWebSocket();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-6">CCTV Monitoring System</h1>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card>
          <div className="flex flex-row items-center justify-between">
            <h2 className="text-lg font-semibold">People Count</h2>
            <Users className="h-6 w-6 text-blue-500" />
          </div>
          <CardContent>
            <p className="text-2xl font-bold">{stats.peopleCount}</p>
          </CardContent>
        </Card>

        <Card>
          <div className="flex flex-row items-center justify-between">
            <h2 className="text-lg font-semibold">Active Alerts</h2>
            <Bell className="h-6 w-6 text-red-500" />
          </div>
          <CardContent>
            <p className="text-2xl font-bold">{stats.alerts.length}</p>
          </CardContent>
        </Card>

        <Card>
          <div className="flex flex-row items-center justify-between">
            <h2 className="text-lg font-semibold">Safety Violations</h2>
            <AlertTriangle className="h-6 w-6 text-yellow-500" />
          </div>
          <CardContent>
            <p className="text-2xl font-bold">{stats.violations.length}</p>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Video Feed */}
        <Card>
          <div className="flex flex-row items-center justify-between">
            <h2 className="text-lg font-semibold">Live Feed</h2>
            <Camera className="h-6 w-6" />
          </div>
          <CardContent>
            <div className="aspect-video bg-black rounded-lg overflow-hidden">
              <img
                src={videoFeed || "/api/placeholder/640/360"}
                alt="CCTV Feed"
                className="w-full h-full object-cover"
              />
            </div>
          </CardContent>
        </Card>

        {/* Crowd Density Chart */}
        <Card>
          <div>
            <h2 className="text-lg font-semibold">Crowd Density Over Time</h2>
          </div>
          <CardContent>
            <LineChart width={500} height={300} data={stats.crowdDensity}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="time" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="density" stroke="#2563eb" />
            </LineChart>
          </CardContent>
        </Card>

        {/* Alerts List */}
        <Card>
          <div>
            <h2 className="text-lg font-semibold">Recent Alerts</h2>
          </div>
          <CardContent>
            <div className="space-y-4">
              {stats.alerts.map((alert, index) => (
                <div key={index} className="flex items-center space-x-4 p-3 bg-red-50 rounded-lg">
                  <AlertTriangle className="h-5 w-5 text-red-500" />
                  <div>
                    <p className="font-medium">{alert.type}</p>
                    <p className="text-sm text-gray-500">{alert.timestamp}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Violations List */}
        <Card>
          <div>
            <h2 className="text-lg font-semibold">Safety Violations</h2>
          </div>
          <CardContent>
            <div className="space-y-4">
              {stats.violations.map((violation, index) => (
                <div key={index} className="flex items-center space-x-4 p-3 bg-yellow-50 rounded-lg">
                  <AlertTriangle className="h-5 w-5 text-yellow-500" />
                  <div>
                    <p className="font-medium">{violation.type}</p>
                    <p className="text-sm text-gray-500">{violation.timestamp}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;