import React from 'react';
import { ArrowUpIcon, ArrowDownIcon, MinusIcon } from '@heroicons/react/24/solid';

function ScalingStatus({ status }) {
  if (!status) return null;

  const getStatusColor = (decision) => {
    switch (decision) {
      case 'scale_up':
        return 'text-red-500';
      case 'scale_down':
        return 'text-green-500';
      default:
        return 'text-gray-500';
    }
  };

  const getStatusIcon = (decision) => {
    switch (decision) {
      case 'scale_up':
        return <ArrowUpIcon className="h-6 w-6 text-red-500" />;
      case 'scale_down':
        return <ArrowDownIcon className="h-6 w-6 text-green-500" />;
      default:
        return <MinusIcon className="h-6 w-6 text-gray-500" />;
    }
  };

  const getStatusDescription = (decision) => {
    switch (decision) {
      case 'scale_up':
        return 'System is scaling up to handle increased load';
      case 'scale_down':
        return 'System is scaling down to optimize resources';
      default:
        return 'System is operating within normal parameters';
    }
  };

  return (
    <div className="bg-white shadow rounded-lg p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">System Status</h3>
      
      {/* Current Status */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm font-medium text-gray-500">Current Status</p>
            <p className={`text-lg font-semibold ${getStatusColor(status.scaling_decision)}`}>
              {status.scaling_decision.replace('_', ' ').toUpperCase()}
            </p>
          </div>
          <div className="flex-shrink-0">
            {getStatusIcon(status.scaling_decision)}
          </div>
        </div>
        <p className="mt-2 text-sm text-gray-500">
          {getStatusDescription(status.scaling_decision)}
        </p>
      </div>

      {/* System Metrics */}
      <div className="border-t border-gray-200 pt-4">
        <h4 className="text-sm font-medium text-gray-500 mb-3">System Metrics</h4>
        <dl className="grid grid-cols-2 gap-4">
          <div>
            <dt className="text-sm text-gray-500">CPU Usage</dt>
            <dd className="mt-1 text-lg font-semibold text-gray-900">
              {status.current_metrics.cpu_usage.toFixed(1)}%
            </dd>
          </div>
          <div>
            <dt className="text-sm text-gray-500">Memory Usage</dt>
            <dd className="mt-1 text-lg font-semibold text-gray-900">
              {status.current_metrics.memory_usage.toFixed(1)}%
            </dd>
          </div>
          <div>
            <dt className="text-sm text-gray-500">Last Prediction</dt>
            <dd className="mt-1 text-lg font-semibold text-gray-900">
              {status.last_prediction ? `${status.last_prediction.toFixed(1)}%` : 'N/A'}
            </dd>
          </div>
          <div>
            <dt className="text-sm text-gray-500">Model Status</dt>
            <dd className="mt-1">
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                status.model_status === 'loaded' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
              }`}>
                {status.model_status.toUpperCase()}
              </span>
            </dd>
          </div>
        </dl>
      </div>

      {/* Last Update */}
      <div className="mt-6 text-sm text-gray-500">
        Last updated: {new Date(status.timestamp).toLocaleString()}
      </div>
    </div>
  );
}

export default ScalingStatus; 