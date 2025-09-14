import datetime
import random
import time

def generate_sample_logs():
    """Generates a sample log file with various anomalies."""
    log_entries = []
    
    # 1. Normal activity
    for i in range(10):
        timestamp = datetime.datetime(2025, 9, 12, 9, 0, 1) + datetime.timedelta(seconds=i * 10)
        log_entries.append(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')},LOGIN_SUCCESS,UserA logged in")

    # 2. Spike Anomaly (multiple LOGIN_FAILURE events for UserC in a short time)
    spike_time = datetime.datetime(2025, 9, 12, 10, 0, 5)
    for i in range(4): # More than X=3 times within Y=5 seconds
        log_entries.append(f"{(spike_time + datetime.timedelta(seconds=i)).strftime('%Y-%m-%d %H:%M:%S')},LOGIN_FAILURE,UserC failed to login")

    # 3. Event Order Violation (LOGOUT before LOGIN)
    logout_before_login_time = datetime.datetime(2025, 9, 12, 10, 15, 0)
    log_entries.append(f"{logout_before_login_time.strftime('%Y-%m-%d %H:%M:%S')},LOGOUT,UserD logged out")
    log_entries.append(f"{(logout_before_login_time + datetime.timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')},LOGIN_SUCCESS,UserD logged in")

    # 4. Gap Anomaly (no events for > Z=5 minutes)
    gap_start_time = datetime.datetime(2025, 9, 12, 10, 20, 0)
    log_entries.append(f"{gap_start_time.strftime('%Y-%m-%d %H:%M:%S')},FILE_UPLOAD,UserA uploaded report.pdf")
    gap_end_time = datetime.datetime(2025, 9, 12, 10, 30, 0) # 10-minute gap
    log_entries.append(f"{gap_end_time.strftime('%Y-%m-%d %H:%M:%S')},LOGIN_SUCCESS,UserE logged in")

    # 5. Out-of-Hours Activity (critical event outside 9 AM - 6 PM)
    off_hours_time = datetime.datetime(2025, 9, 12, 23, 45, 0)
    log_entries.append(f"{off_hours_time.strftime('%Y-%m-%d %H:%M:%S')},FILE_DELETE,UserB deleted secret.txt")


    
    with open("sample_log.log", "w") as f:
        for entry in log_entries:
            f.write(entry + "\n")

    print("Sample log file 'sample_log.log' created successfully.")

if __name__ == "__main__":
    generate_sample_logs()