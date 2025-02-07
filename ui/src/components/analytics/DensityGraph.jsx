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

const DensityGraph = () => {
  const data = {
    labels: ["10:00", "11:00", "12:00", "13:00", "14:00"],
    datasets: [
      {
        label: "Crowd Density",
        data: [0.2, 0.3, 0.5, 0.4, 0.6],
        fill: false,
        backgroundColor: "rgb(75, 192, 192)",
        borderColor: "rgba(75, 192, 192, 0.6)",
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
          label: (context) => `Density: ${context.parsed.y.toFixed(2)}`,
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 1, // Normalize density to a scale of 0-1
        ticks: {
          color: "#6B7280", // Subtle gray text
          callback: (value) => `${(value * 100).toFixed(0)}%`, // Display as percentage
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
        <CardTitle className="text-xl font-bold">Crowd Density Over Time</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="h-[300px]">
          <Line data={data} options={options} />
        </div>
      </CardContent>
    </Card>
  );
};

export default DensityGraph;