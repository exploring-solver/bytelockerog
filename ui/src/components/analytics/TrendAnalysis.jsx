"use client"; // Required for Client Components in Next.js App Router

import React from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

const TrendAnalysis = () => {
  const data = {
    labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    datasets: [
      {
        label: "Anomalies Detected",
        data: [2, 3, 1, 4, 2],
        fill: false,
        backgroundColor: "rgb(255, 99, 132)",
        borderColor: "rgba(255, 99, 132, 0.6)",
        tension: 0.4, // Smooth curve effect
        pointRadius: 5, // Larger points for better visibility
        pointHoverRadius: 7, // Hover effect
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      tooltip: {
        callbacks: {
          label: (context) => `${context.parsed.y} anomalies`,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          color: "#6B7280", // Subtle gray text
        },
      },
      x: {
        ticks: {
          color: "#6B7280", // Subtle gray text
        },
      },
    },
  };

  return (
    <Card className="shadow-lg">
      <CardHeader>
        <CardTitle className="text-xl font-bold">Weekly Anomaly Trends</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[300px]">
          <Line data={data} options={options} />
        </div>
      </CardContent>
    </Card>
  );
};

export default TrendAnalysis;