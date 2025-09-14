import datetime

# Define detection thresholds
SPIKE_THRESHOLD_COUNT = 3  # X times
SPIKE_THRESHOLD_SECONDS = 5 # Y seconds
GAP_THRESHOLD_MINUTES = 5   # Z minutes
BUSINESS_START_HOUR = 9
BUSINESS_END_HOUR = 18

def detect_anomalies(log_entries):
    """
    Detects various anomalies in a list of log entries.
    
    Args:
        log_entries (list): A list of parsed log dictionaries.
        
    Returns:
        list: A list of dictionaries, each describing a detected anomaly.
    """
    anomalies = []
    
    # Track user states for order violation
    user_sessions = {}
    
    # Spike and Gap Anomaly detection
    event_counts = {}
    
    for i, entry in enumerate(log_entries):
        timestamp = entry['timestamp']
        activity = entry['activity']
        message = entry['message']
        
        # Spike Anomaly Check
        if activity not in event_counts:
            event_counts[activity] = []
        
        event_counts[activity].append(timestamp)
        
        # Remove timestamps outside the sliding window
        event_counts[activity] = [t for t in event_counts[activity] if (timestamp - t).total_seconds() <= SPIKE_THRESHOLD_SECONDS]
        
        if len(event_counts[activity]) > SPIKE_THRESHOLD_COUNT:
            anomalies.append({
                "type": "Spike Anomaly",
                "event": activity,
                "time_range": f"{event_counts[activity][0].strftime('%Y-%m-%d %H:%M:%S')} - {event_counts[activity][-1].strftime('%Y-%m-%d %H:%M:%S')}",
                "count": len(event_counts[activity]),
                "description": f"A spike of {len(event_counts[activity])} '{activity}' events occurred within a {SPIKE_THRESHOLD_SECONDS} second window."
            })
            # Clear the list to avoid duplicate reporting for the same spike
            event_counts[activity] = []

        # Gap Anomaly Check
        if i > 0:
            previous_timestamp = log_entries[i-1]['timestamp']
            time_diff_minutes = (timestamp - previous_timestamp).total_seconds() / 60
            if time_diff_minutes > GAP_THRESHOLD_MINUTES:
                anomalies.append({
                    "type": "Gap Anomaly",
                    "time_range": f"{previous_timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
                    "duration_minutes": round(time_diff_minutes, 2),
                    "description": f"No events were recorded for a duration of {round(time_diff_minutes, 2)} minutes."
                })

        # Event Order Violation Check
        user = message.split()[0]
        if 'LOGIN_SUCCESS' in activity:
            user_sessions[user] = 'logged_in'
        elif 'LOGOUT' in activity:
            if user not in user_sessions or user_sessions[user] != 'logged_in':
                anomalies.append({
                    "type": "Event Order Violation",
                    "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    "user": user,
                    "event": activity,
                    "description": f"User '{user}' attempted to {activity} without a prior successful login."
                })
            else:
                user_sessions[user] = 'logged_out'

        # Out-of-Hours Activity Check
        if 'FILE' in activity or 'DELETE' in activity or 'UPLOAD' in activity: # Critical events
       
            if not (BUSINESS_START_HOUR <= timestamp.hour < BUSINESS_END_HOUR):
                anomalies.append({
                    "type": "Out-of-Hours Activity",
                    "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    "event": activity,
                    "user": user,
                    "description": f"Critical event '{activity}' occurred outside of business hours (9AM-6PM)."
                })

    return anomalies