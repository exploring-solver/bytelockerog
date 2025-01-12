// src/services/api.js
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

export const api = {
  async getCameras() {
    const response = await fetch(`${API_BASE_URL}/api/cameras`);
    return response.json();
  },

  async getMetrics(timeRange) {
    const response = await fetch(`${API_BASE_URL}/api/metrics?timeRange=${timeRange}`);
    return response.json();
  },

  async getAlerts(filters) {
    const queryParams = new URLSearchParams(filters);
    const response = await fetch(`${API_BASE_URL}/api/alerts?${queryParams}`);
    return response.json();
  },

  async updateSettings(settings) {
    const response = await fetch(`${API_BASE_URL}/api/settings`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(settings),
    });
    return response.json();
  },
};