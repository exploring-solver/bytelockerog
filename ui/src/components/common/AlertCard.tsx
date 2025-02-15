import { AlertCircle, AlertTriangle, Info, ChevronDown, ChevronUp } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

const getAlertIcon = (severity: string) => {
  switch (severity) {
    case 'high':
      return <AlertCircle className="h-5 w-5 text-destructive" />;
    case 'medium':
      return <AlertTriangle className="h-5 w-5 text-warning" />;
    default:
      return <Info className="h-5 w-5 text-info" />;
  }
};

const getSeverityColor = (severity: string) => {
  switch (severity) {
    case 'high':
      return 'bg-destructive/10 text-destructive hover:bg-destructive/20';
    case 'medium':
      return 'bg-warning/10 text-warning hover:bg-warning/20';
    default:
      return 'bg-sky-500/10 text-sky-500 hover:bg-sky-500/20';
  }
};

const AlertCard = ({ alert, expanded, onClick }) => {
  return (
    <div 
      onClick={onClick}
      className={cn(
        "p-4 rounded-lg border transition-all duration-200",
        "hover:bg-accent/50 cursor-pointer",
        expanded ? "bg-accent/30" : "bg-background"
      )}
    >
      <div className="flex items-start gap-3">
        <div className="mt-1">{getAlertIcon(alert.severity)}</div>
        
        <div className="flex-1 space-y-1">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <h4 className="font-medium">{alert.type}</h4>
              <Badge variant="outline" className={getSeverityColor(alert.severity)}>
                {alert.severity}
              </Badge>
              {alert.resolved && (
                <Badge variant="outline" className="bg-emerald-500/10 text-emerald-500">
                  Resolved
                </Badge>
              )}
            </div>
            {expanded ? 
              <ChevronUp className="h-5 w-5 text-muted-foreground" /> : 
              <ChevronDown className="h-5 w-5 text-muted-foreground" />
            }
          </div>
          
          <div className="flex gap-3 text-sm text-muted-foreground">
            <span>{new Date(alert.timestamp).toLocaleString()}</span>
            <span>•</span>
            <span>{alert.location}</span>
          </div>
          
          {expanded && (
            <div className="mt-3 pt-3 border-t">
              <p className="text-sm text-muted-foreground">{alert.details}</p>
              {alert.facesDetected?.length > 0 && (
                <div className="mt-2 flex items-center gap-2 text-sm text-muted-foreground">
                  <span>Detected:</span>
                  <span className="font-medium">{alert.facesDetected.join(', ')}</span>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AlertCard;