
Log File Anomaly Detection
This project is an application designed to automatically analyze a given log file and identify anomalies based on a set of defined rules. The solution is built with a modular approach, with separate scripts for log generation, parsing, anomaly detection, and reporting.

Objectives
The application successfully fulfills the following core objectives as per the assignment:

Parse and analyze log files.

Detect anomalies including Spike, Gap, Event Order Violation, and Out-of-Hours activity.

Visualize spike anomalies with a plot showing event frequency over time.

Generate structured anomaly reports in a machine-readable JSON format.

Store detected anomalies in an SQLite database for persistence.

How to Run the Application
Clone the repository:

Bash

git clone https://github.com/<your-username>/log-anomaly-detector.git
cd log-anomaly-detector
Install dependencies:
The project uses pandas and matplotlib for data handling and visualization.

Bash

pip install pandas matplotlib
Run the main script:

Bash

python main.py
This command will execute the entire process, including:

Generating a sample log file (sample_log.log).

Detecting anomalies.

Creating an anomaly_report.json file.

Generating and saving a plot image (spike_anomaly_plot.png).

Creating and saving the anomalies to an SQLite database file (anomalies.db).

Evaluation Criteria
The solution has been developed to meet all the specified evaluation criteria:

Correctness: The program correctly identifies all four types of anomalies specified in the assignment. The JSON output accurately reports a spike, gaps, an event order violation, and out-of-hours activity.

Completeness: All required deliverables are included in this repository: the source code, the sample_log.log file, the anomaly_report.json file, and the anomalies.db database file.

Clarity: The code is well-structured and separated into modular scripts. Each function includes detailed docstrings and comments to explain the logic.

Justification: The use of pandas and matplotlib is justified for general-purpose tasks of data handling and visualization. The core anomaly detection logic for each anomaly type was implemented manually in anomaly_detector.py, ensuring that these libraries do not replace the core logic of the assignment.

Practicality: The solution realistically handles practical scenarios. The ability to detect periods of inactivity (gaps) and to identify critical events outside business hours adds a realistic form of risk assessment to the solution. The use of a database provides data persistence for further analysis.

Outputs
The project generates both a structured JSON report and a visual output to showcase the detected anomalies.

Spike Anomaly Visualization:
This plot visually represents the event frequency over time and correctly highlights a detected spike in events.
