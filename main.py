import json
import matplotlib.pyplot as plt
import pandas as pd
from log_parser import parse_log_file
from anomaly_detector import detect_anomalies
import sqlite3

def generate_report(anomalies, output_file="anomaly_report.json"):
    """
    Generates a structured, machine-readable JSON report of detected anomalies.
    
    Args:
        anomalies (list): A list of anomaly dictionaries.
        output_file (str): The path for the output JSON file.
    """
    with open(output_file, 'w') as f:
        json.dump(anomalies, f, indent=4)
    print(f"Anomaly report generated and saved to '{output_file}'")

def visualize_spikes(log_entries, detected_anomalies):
    """
    Visualizes event frequencies and marks detected spikes.
    
    Args:
        log_entries (list): All parsed log entries.
        detected_anomalies (list): List of detected anomaly dictionaries.
    """
    # Create a DataFrame for easy plotting using pandas
    df = pd.DataFrame(log_entries)
    df.set_index('timestamp', inplace=True)
    
    # Resample to get event frequency per minute. Use 'min' for clarity
    event_freq = df.resample('min').size().fillna(0)
    
    # Plotting using matplotlib
    plt.figure(figsize=(12, 6))
    event_freq.plot(marker='o', linestyle='-')
    
    spike_anomalies = [a for a in detected_anomalies if a['type'] == 'Spike Anomaly']
    for spike in spike_anomalies:
        time_range = spike['time_range'].split(' - ')
        start_time = pd.to_datetime(time_range[0])
        end_time = pd.to_datetime(time_range[1])
        
        # Mark the spike area in red with a semi-transparent rectangle
        plt.axvspan(start_time, end_time, color='red', alpha=0.3, label='Spike Anomaly')
        
        # Correctly get the y-value for the text label using a time bin
        y_pos = event_freq.loc[start_time.floor('min')]
        plt.text(start_time, y_pos, 'Spike', color='red', ha='center', va='bottom')
    
    plt.title('Event Frequency Over Time with Detected Spikes')
    plt.xlabel('Time')
    plt.ylabel('Number of Events')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
     # Add this line to save the plot before showing it
    plt.savefig('spike_anomaly_plot.png')
    plt.show()

def save_anomalies_to_db(anomalies, db_file="anomalies.db"):
    """
    Saves detected anomalies into an SQLite database file.

    Args:
        anomalies (list): A list of dictionaries, where each dict is a detected anomaly.
        db_file (str): The name of the SQLite database file to create.
    """
    try:
        # Connect to the SQLite database file
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Create a table to store the anomalies
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                event TEXT,
                timestamp TEXT,
                time_range TEXT,
                duration_minutes REAL,
                count INTEGER,
                user TEXT,
                description TEXT
            )
        ''')

        # Insert each anomaly into the database table
        for anomaly in anomalies:
            cursor.execute('''
                INSERT INTO anomalies (type, event, timestamp, time_range, duration_minutes, count, user, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                anomaly.get('type'),
                anomaly.get('event'),
                anomaly.get('timestamp'),
                anomaly.get('time_range'),
                anomaly.get('duration_minutes'),
                anomaly.get('count'),
                anomaly.get('user'),
                anomaly.get('description')
            ))
        
        conn.commit()
        print(f"Anomalies successfully saved to '{db_file}'")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # The main execution block of the program
    
    # 1. Parse the log file
    log_file_path = "sample_log.log"
    log_data = parse_log_file(log_file_path)

    # 2. Detect anomalies
    anomalies = detect_anomalies(log_data)

    # 3. Generate structured report
    generate_report(anomalies)

    # 4. Save anomalies to database (Optional)
    save_anomalies_to_db(anomalies)

    # 5. Visualize spike anomalies
    visualize_spikes(log_data, anomalies)