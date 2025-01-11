import React, { useState, useEffect, useRef } from 'react';
// import { Card, CardContent } from '@/components/ui/card';
import { Camera } from 'lucide-react';

const VideoFeed = () => {
  const [imageUrl, setImageUrl] = useState(null);
  const eventSourceRef = useRef(null);

  useEffect(() => {
    // Create EventSource for Server-Sent Events
    eventSourceRef.current = new EventSource('http://localhost:8000/video-feed');

    eventSourceRef.current.onmessage = (event) => {
      setImageUrl(event.data);
    };

    eventSourceRef.current.onerror = (error) => {
      console.error('EventSource error:', error);
      eventSourceRef.current.close();
      // Attempt to reconnect after 5 seconds
      setTimeout(() => {
        eventSourceRef.current = new EventSource('http://localhost:8000/video-feed');
      }, 5000);
    };

    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  return (
    <div className="w-full">
      <div className="p-4 flex flex-row items-center justify-between">
        <h2 className="text-lg font-semibold">Live Feed</h2>
        <Camera className="h-6 w-6" />
      </div>
      <div>
        <div className="aspect-video bg-black rounded-lg overflow-hidden">
          {imageUrl ? (
            <img
              src={imageUrl}
              alt="CCTV Feed"
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-white">
              Loading video feed...
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default VideoFeed;