"use client"; // Required for Client Components in Next.js App Router

import React, { useState } from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  
} from "@/components/ui/card";
import { Button } from "../ui/button";
import { Badge } from "@/components/ui/badge";
import { ChevronDown, ChevronUp, Trash2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const mockAnomalies = [
  {
    id: 1,
    type: "Unauthorized Access",
    timestamp: "2023-10-01T10:15:00",
    details: "Person detected in restricted area",
    facesDetected: ["John Doe", "Jane Smith"],
  },
  {
    id: 2,
    type: "Proximity Alert",
    timestamp: "2023-10-01T11:00:00",
    details: "Multiple people detected in close proximity",
    facesDetected: ["Alice Johnson"],
  },
  {
    id: 3,
    type: "Loitering",
    timestamp: "2023-10-01T12:30:00",
    details: "Person loitering near entrance for over 10 minutes",
    facesDetected: ["Unknown"],
  },
];

const AnomaliesList = () => {
  const [expanded, setExpanded] = useState(null);
  const [anomalies, setAnomalies] = useState(mockAnomalies);

  const handleToggle = (id) => {
    setExpanded(expanded === id ? null : id);
  };

  const handleClearAll = () => {
    setAnomalies([]);
    setExpanded(null);
  };

  return (
    <Card className="shadow-lg">
      <CardHeader>
        <div className="flex justify-between items-center">
          <CardTitle className="text-xl font-bold">Detected Anomalies</CardTitle>
          <Button
            variant="destructive"
            size="sm"
            onClick={handleClearAll}
            disabled={anomalies.length === 0}
            className="flex items-center gap-2"
          >
            <Trash2 size={16} />
            Clear All
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {anomalies.length === 0 ? (
          <p className="text-gray-500 text-center py-4">No anomalies detected.</p>
        ) : (
          <ul className="space-y-4">
            {anomalies.map((anomaly) => (
              <li key={anomaly.id}>
                <div
                  className="bg-gray-50 p-4 rounded-lg shadow-sm cursor-pointer hover:bg-gray-100 transition-colors"
                  onClick={() => handleToggle(anomaly.id)}
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <h3 className="font-semibold">{anomaly.type}</h3>
                      <p className="text-sm text-gray-500">
                        Detected at:{" "}
                        {new Date(anomaly.timestamp).toLocaleString()}
                      </p>
                    </div>
                    <Badge
                      variant={
                        anomaly.type === "Unauthorized Access"
                          ? "destructive"
                          : anomaly.type === "Proximity Alert"
                          ? "warning"
                          : "default"
                      }
                      className="capitalize"
                    >
                      {anomaly.type.split(" ")[0]}
                    </Badge>
                    <button onClick={() => handleToggle(anomaly.id)}>
                      {expanded === anomaly.id ? (
                        <ChevronUp size={20} />
                      ) : (
                        <ChevronDown size={20} />
                      )}
                    </button>
                  </div>
                  <AnimatePresence>
                    {expanded === anomaly.id && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3 }}
                        className="mt-4 space-y-2"
                      >
                        <p className="text-sm text-gray-700">
                          {anomaly.details}
                        </p>
                        <p className="text-sm text-gray-700">
                          Faces Detected:{" "}
                          {anomaly.facesDetected.join(", ") || "N/A"}
                        </p>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
};

export default AnomaliesList;