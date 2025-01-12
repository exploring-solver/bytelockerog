// src/utils/helpers.js
export const formatDate = (date) => {
    return new Date(date).toLocaleString();
  };
  
  export const calculateCrowdDensity = (count, area) => {
    return (count / area) * 100;
  };
  
  export const getAlertSeverity = (value, threshold) => {
    if (value >= threshold.high) return 'high';
    if (value >= threshold.medium) return 'medium';
    return 'low';
  };
  
  export const formatMetric = (value, type) => {
    switch (type) {
      case 'percentage':
        return `${(value * 100).toFixed(1)}%`;
      case 'number':
        return value.toLocaleString();
      case 'time':
        return new Date(value).toLocaleString();
      default:
        return value;
    }
  };