### Repository Description:
**client-server-resource-monitoring**

A Python-based client-server system designed for real-time monitoring and management of CPU, GPU, memory, and temperature utilization. This project allows two client devices to measure and send their resource data to a server, which processes and displays the information on a web page. Clients also have the ability to set thresholds for the parameters of the other client, with the server providing visual alerts (color changes) when the thresholds are exceeded.

### Key Features:
- **Real-time monitoring**: Continuously track CPU, GPU, memory utilization, and temperature.
- **Multithreaded server**: The server handles data from multiple clients simultaneously using multithreading.
- **Web interface**: Clients can view live data and set thresholds via a user-friendly web page.
- **Visual alerts**: The server highlights any values that exceed the set thresholds in red for easy identification.
- **Retry logic**: Clients automatically retry connections if the server is unreachable, with a defined timeout after several failed attempts.

### Installation:
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/client-server-resource-monitoring.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python server.py
   ```
4. Run the client on separate devices:
   ```bash
   python client.py
   ```

### Requirements:
- Python 3.x
- Flask
- Psutil (system resource monitoring)
- PyNVML (GPU resource monitoring)

### File Structure:
```
client-server-resource-monitoring/
├── server.py               # Server-side logic (multithreading, data handling)
├── client.py               # Client-side logic (resource collection, data sending)
├── templates/
│   └── index.html          # HTML template for displaying resource data
├── static/
│   └── styles.css          # CSS for the dashboard
├── requirements.txt        # Required Python packages
└── README.md               # Project documentation
```
