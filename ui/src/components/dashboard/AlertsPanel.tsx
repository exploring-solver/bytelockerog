import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import AlertCard from "@/components/common/AlertCard";
const AlertsPanel = ({ alerts }) => {
  const [expandedId, setExpandedId] = useState(null);

  const handleExpand = (id) => {
    setExpandedId(expandedId === id ? null : id);
  };

  return (
    <Card className=''>
      <CardHeader>
        <CardTitle className='text-black'>Recent Alerts</CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[400px] ">
          <div className="space-y-3">
            {alerts.map((alert) => (
              <AlertCard
                key={alert.id}
                alert={alert}
                expanded={expandedId === alert.id}
                onClick={() => handleExpand(alert.id)}
              />
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};

export default AlertsPanel;