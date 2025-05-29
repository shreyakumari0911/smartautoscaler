from prometheus_client import Gauge, Counter

# System metrics
cpu_usage_gauge = Gauge(
    'cpu_usage_percent',
    'Current CPU usage percentage',
    ['instance']
)

memory_usage_gauge = Gauge(
    'memory_usage_percent',
    'Current memory usage percentage',
    ['instance']
)

# ML prediction metrics
prediction_gauge = Gauge(
    'predicted_cpu_usage',
    'Predicted CPU usage for next 5 minutes',
    ['instance']
)

# Scaling action metrics
scaling_action_counter = Counter(
    'scaling_actions_total',
    'Total number of scaling actions taken',
    ['action', 'instance']
)

# Initialize instance labels
instance_label = {'instance': 'smartscaling'}

cpu_usage_gauge.labels(**instance_label)
memory_usage_gauge.labels(**instance_label)
prediction_gauge.labels(**instance_label)
scaling_action_counter.labels(action='scale_up', **instance_label)
scaling_action_counter.labels(action='scale_down', **instance_label)
scaling_action_counter.labels(action='no_action', **instance_label) 