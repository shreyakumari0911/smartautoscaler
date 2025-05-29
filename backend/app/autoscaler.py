import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

# Scaling thresholds
SCALE_UP_THRESHOLD = 80.0  # Scale up if CPU usage is above 80%
SCALE_DOWN_THRESHOLD = 30.0  # Scale down if CPU usage is below 30%
PREDICTION_WEIGHT = 0.7  # Weight given to predicted CPU in decision making

def get_scaling_decision(current_cpu: float, predicted_cpu: Optional[float] = None) -> str:
    """
    Make a scaling decision based on current and predicted CPU usage.
    
    Args:
        current_cpu: Current CPU usage percentage
        predicted_cpu: Predicted CPU usage percentage (optional)
    
    Returns:
        Scaling decision: 'scale_up', 'scale_down', or 'no_action'
    """
    try:
        # If we have a prediction, use weighted average
        if predicted_cpu is not None:
            weighted_cpu = (current_cpu * (1 - PREDICTION_WEIGHT) + 
                          predicted_cpu * PREDICTION_WEIGHT)
            logger.info(f"Using weighted CPU: {weighted_cpu:.2f}% "
                       f"(current: {current_cpu:.2f}%, predicted: {predicted_cpu:.2f}%)")
        else:
            weighted_cpu = current_cpu
            logger.info(f"No prediction available, using current CPU: {current_cpu:.2f}%")
        
        # Make scaling decision
        if weighted_cpu > SCALE_UP_THRESHOLD:
            decision = "scale_up"
            logger.info(f"Decision: {decision} (weighted CPU: {weighted_cpu:.2f}% > {SCALE_UP_THRESHOLD}%)")
        elif weighted_cpu < SCALE_DOWN_THRESHOLD:
            decision = "scale_down"
            logger.info(f"Decision: {decision} (weighted CPU: {weighted_cpu:.2f}% < {SCALE_DOWN_THRESHOLD}%)")
        else:
            decision = "no_action"
            logger.info(f"Decision: {decision} (weighted CPU: {weighted_cpu:.2f}% within thresholds)")
        
        return decision
        
    except Exception as e:
        logger.error(f"Error making scaling decision: {e}")
        return "no_action"

def simulate_scaling_action(decision: str) -> bool:
    """
    Simulate a scaling action. In a real scenario, this would interact with
    a cloud provider's API to actually scale resources.
    
    Args:
        decision: The scaling decision ('scale_up', 'scale_down', or 'no_action')
    
    Returns:
        True if the action was successful, False otherwise
    """
    try:
        if decision == "no_action":
            logger.info("No scaling action needed")
            return True
            
        # Simulate API call to cloud provider
        logger.info(f"Simulating {decision} action...")
        
        # Simulate some processing time
        import time
        time.sleep(1)
        
        logger.info(f"Successfully simulated {decision}")
        return True
        
    except Exception as e:
        logger.error(f"Error simulating scaling action: {e}")
        return False

if __name__ == "__main__":
    # Example usage
    current_cpu = 85.0
    predicted_cpu = 90.0
    
    decision = get_scaling_decision(current_cpu, predicted_cpu)
    success = simulate_scaling_action(decision)
    
    print(f"Decision: {decision}")
    print(f"Action successful: {success}") 