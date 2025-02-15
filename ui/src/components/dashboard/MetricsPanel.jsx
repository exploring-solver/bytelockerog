import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { 
  Users, 
  AlertTriangle, 
  BarChart2, 
  TrendingUp, 
  Clock,
  ShieldCheck 
} from "lucide-react";

const MetricCard = ({ icon: Icon, title, value, color = "text-primary" }) => (
  <div className="flex items-center p-1 bg-card rounded-lg border shadow-sm transition-all duration-200 hover:shadow-md">
    <div className={`${color} p-2 rounded-full bg-background`}>
      <Icon className="h-6 w-6" />
    </div>
    <div className="ml-4">
      <p className="text-sm font-medium text-muted-foreground">{title}</p>
      <h3 className="text-2xl font-bold tracking-tight">{value}</h3>
    </div>
  </div>
);

const MetricsPanel = ({ metrics }) => {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="text-xl font-semibold">Metrics Overview</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          <MetricCard
            icon={Users}
            title="Total People"
            value={metrics.totalPeople.toLocaleString()}
            color="text-blue-500"
          />
          
          <MetricCard
            icon={BarChart2}
            title="Current Density"
            value={`${(metrics.crowdDensity * 100).toFixed(1)}%`}
            color="text-amber-500"
          />
          
          <MetricCard
            icon={AlertTriangle}
            title="Active Alerts"
            value={metrics.alerts.length}
            color="text-red-500"
          />

          <div className="md:col-span-2 lg:col-span-2 p-2 bg-card rounded-lg border shadow-sm">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center">
                <ShieldCheck className="h-5 w-5 text-green-500 mr-2" />
                <h3 className="text-sm font-medium text-muted-foreground">Safety Score</h3>
              </div>
              <span className="text-2xl font-bold">{metrics.safetyScore}%</span>
            </div>
            <Progress 
              value={metrics.safetyScore} 
              className={`h-2 ${
                metrics.safetyScore > 80 ? 'bg-green-100' : 'bg-amber-100'
              }`}
            />
          </div>

          <div className="p-2 bg-card rounded-lg border shadow-sm">
            <div className="flex items-center space-x-4">
              <div className="p-2 rounded-full bg-background text-blue-500">
                <Clock className="h-6 w-6" />
              </div>
              <div>
                <p className="text-sm font-medium text-muted-foreground">Peak Hour</p>
                <div className="flex items-baseline space-x-2">
                  <h3 className="text-2xl font-bold tracking-tight">{metrics.peakHour}:00</h3>
                  <TrendingUp className="h-4 w-4 text-green-500" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default MetricsPanel;