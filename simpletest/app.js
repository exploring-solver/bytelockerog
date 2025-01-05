document.addEventListener('DOMContentLoaded', () => {
    const peopleCountElement = document.getElementById('people-count');
    const activeAlertsElement = document.getElementById('active-alerts');
    const safetyViolationsElement = document.getElementById('safety-violations');
    const ctx = document.getElementById('crowd-density-chart').getContext('2d');

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Crowd Density',
                data: [],
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'second'
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const ws = new WebSocket('ws://localhost:8000/ws/metrics');

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        peopleCountElement.textContent = data.peopleCount;
        activeAlertsElement.textContent = data.alerts.length;
        safetyViolationsElement.textContent = data.violations.length;

        // Update crowd density chart
        const newTime = data.crowdDensity[0].time;
        const newDensity = data.crowdDensity[0].density;
        chart.data.labels.push(newTime);
        chart.data.datasets[0].data.push(newDensity);

        // Keep only the last 10 data points
        if (chart.data.labels.length > 10) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
        }

        chart.update();
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
        console.log('WebSocket connection closed');
    };
});
