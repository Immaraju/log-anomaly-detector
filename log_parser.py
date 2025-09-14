import datetime
import re

def parse_log_file(file_path):
    """
    Reads a log file and parses each line into a structured dictionary.
    
    Args:
        file_path (str): The path to the log file.
        
    Returns:
        list: A list of dictionaries, where each dict represents a log entry.
    """
    parsed_logs = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',', 2)
            if len(parts) == 3:
                try:
                    # Parse timestamp, activity, and message
                    timestamp = datetime.datetime.strptime(parts[0], "%Y-%m-%d %H:%M:%S")
                    activity = parts[1]
                    message = parts[2]
                    parsed_logs.append({
                        'timestamp': timestamp,
                        'activity': activity,
                        'message': message
                    })
                except (ValueError, IndexError) as e:
                    print(f"Skipping malformed line: {line.strip()} - {e}")
    return sorted(parsed_logs, key=lambda x: x['timestamp'])