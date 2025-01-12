// src/services/websocket.js
class WebSocketService {
    constructor() {
      this.ws = null;
      this.subscribers = new Set();
    }
  
    connect(url) {
      this.ws = new WebSocket(url);
  
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.subscribers.forEach(callback => callback(data));
      };
  
      this.ws.onclose = () => {
        setTimeout(() => this.connect(url), 5000); // Reconnect after 5 seconds
      };
    }
  
    subscribe(callback) {
      this.subscribers.add(callback);
      return () => this.subscribers.delete(callback);
    }
  
    disconnect() {
      if (this.ws) {
        this.ws.close();
      }
    }
  }
  
  export const wsService = new WebSocketService();