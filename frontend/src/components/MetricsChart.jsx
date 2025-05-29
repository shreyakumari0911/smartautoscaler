import React, { useEffect, useRef, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const MAX_DATA_POINTS = 20;

function MetricsChart({ metrics, prediction }) {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Current CPU Usage',
        data: [],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
        tension: 0.4,
      },
      {
        label: 'Predicted CPU Usage',
        data: [],
        borderColor: 'rgb(16, 185, 129)',
        backgroundColor: 'rgba(16, 185, 129, 0.5)',
        borderDash: [5, 5],
        tension: 0.4,
      },
    ],
  });

  const chartRef = useRef(null);

  useEffect(() => {
    if (!metrics || !prediction) return;

    const timestamp = new Date(metrics.timestamp).toLocaleTimeString();
    
    setChartData(prevData => {
      const newLabels = [...prevData.labels, timestamp].slice(-MAX_DATA_POINTS);
      const newCurrentData = [...prevData.datasets[0].data, metrics.cpu_usage].slice(-MAX_DATA_POINTS);
      const newPredictedData = [...prevData.datasets[1].data, prediction.predicted_cpu].slice(-MAX_DATA_POINTS);

      return {
        labels: newLabels,
        datasets: [
          {
            ...prevData.datasets[0],
            data: newCurrentData,
          },
          {
            ...prevData.datasets[1],
            data: newPredictedData,
          },
        ],
      };
    });
  }, [metrics, prediction]);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'CPU Usage Over Time',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: 'CPU Usage (%)',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Time',
        },
      },
    },
    animation: {
      duration: 0, // Disable animation for better performance
    },
  };

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="h-80">
        <Line ref={chartRef} data={chartData} options={options} />
      </div>
      <div className="mt-4 grid grid-cols-2 gap-4">
        <div className="text-center">
          <p className="text-sm text-gray-500">Current CPU</p>
          <p className="text-lg font-semibold text-blue-500">
            {metrics?.cpu_usage.toFixed(1)}%
          </p>
        </div>
        <div className="text-center">
          <p className="text-sm text-gray-500">Predicted CPU</p>
          <p className="text-lg font-semibold text-green-500">
            {prediction?.predicted_cpu.toFixed(1)}%
          </p>
        </div>
      </div>
    </div>
  );
}

export default MetricsChart; 