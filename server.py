import socket
import threading
from flask import Flask, render_template, request
from flask import Flask, render_template, request, redirect, url_for

# Data storage for client resource utilization and thresholds
client_data = {
    "Client A": {"CPU_UTIL": 0, "MEMORY_UTIL": 0, "GPU_UTIL": 0, "GPU_TEMP": 0},
    "Client B": {"CPU_UTIL": 0, "MEMORY_UTIL": 0, "GPU_UTIL": 0, "GPU_TEMP": 0},
}
thresholds = {
    "Client A": {"CPU_UTIL": 80, "MEMORY_UTIL": 90, "GPU_UTIL": 80, "GPU_TEMP": 85},
    "Client B": {"CPU_UTIL": 80, "MEMORY_UTIL": 90, "GPU_UTIL": 80, "GPU_TEMP": 85},
}

# Flask App for Server
app = Flask(__name__)

# Socket server settings
HOST = "0.0.0.0"
PORT = 12346


def parse_client_data(data_text):
    """Parses plain-text data into a dictionary."""
    try:
        # Example format: "CPU_UTIL:50,MEMORY_UTIL:30,GPU_UTIL:70,GPU_TEMP:60"
        data_parts = data_text.split(",")
        parsed_data = {}
        for part in data_parts:
            key, value = part.split(":")
            parsed_data[key.strip()] = float(value.strip())
        return parsed_data
    except Exception as e:
        print(f"Error parsing data: {e}")
        return {}


def handle_client(client_socket, client_name):
    """Handles incoming data from a client."""
    try:
        while True:
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                break

            print(f"Received data from {client_name}: {data}")

            # Parse the plain-text data
            parsed_data = parse_client_data(data)
            if parsed_data:
                client_data[client_name].update(parsed_data)
                print(f"Updated {client_name} data: {client_data[client_name]}")
    except Exception as e:
        print(f"Error with {client_name}: {e}")
    finally:
        client_socket.close()


def socket_server():
    """Sets up the socket server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Server listening on {HOST}:{PORT}...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")

            
            client_name = "Client A" if addr[0] == "127.0.0.1" else "Client B"
            threading.Thread(target=handle_client, args=(client_socket, client_name)).start()


@app.route("/")
def index():
    """Renders the monitoring dashboard."""
    return render_template("index.html", data=client_data, thresholds=thresholds)


@app.route("/set_thresholds", methods=["POST"])
def set_thresholds():
    """Updates thresholds from user input."""
    try:
        client = request.form["client"]

        # Update thresholds only for fields that are filled
        if client not in thresholds:
            return f"Client {client} does not exist.", 400

        if "cpu" in request.form and request.form["cpu"]:
            cpu = float(request.form["cpu"])
            if 0 <= cpu <= 100:
                thresholds[client]["CPU_UTIL"] = cpu
            else:
                return "CPU value must be between 0 and 100.", 400

        if "memory" in request.form and request.form["memory"]:
            memory = float(request.form["memory"])
            if 0 <= memory <= 100:
                thresholds[client]["MEMORY_UTIL"] = memory
            else:
                return "Memory value must be between 0 and 100.", 400

        if "gpu" in request.form and request.form["gpu"]:
            gpu = float(request.form["gpu"])
            if 0 <= gpu <= 100:
                thresholds[client]["GPU_UTIL"] = gpu
            else:
                return "GPU value must be between 0 and 100.", 400

        if "gpu_temp" in request.form and request.form["gpu_temp"]:
            gpu_temp = float(request.form["gpu_temp"])
            if 0 <= gpu_temp <= 100:
                thresholds[client]["GPU_TEMP"] = gpu_temp
            else:
                return "GPU Temp value must be between 0 and 100.", 400

        # Redirect back to the monitoring page
        return redirect(url_for("index"))

    except KeyError as e:
        return f"Missing form field: {e}", 400
    except ValueError as e:
        return f"Invalid input: {e}. Please enter a number between 0 and 100.", 400
    except Exception as e:
        return f"An error occurred: {e}", 500



if __name__ == "__main__":
    # Start socket server in a separate thread
    threading.Thread(target=socket_server, daemon=True).start()

    # Start Flask app for web interface
    app.run(host="0.0.0.0", port=5000)
