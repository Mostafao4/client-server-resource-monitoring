import psutil
import socket 
import subprocess
import time


def get_pc_data():
    # Get CPU utilization
    def get_cpu_utilization():
        return psutil.cpu_percent() 
    
    # Get memory utilization
    def get_memory_utilization():
        return psutil.virtual_memory().percent

    # Get GPU utilization and temperature
    def get_gpu_utilization_and_temperature():
        try:
            # Run `nvidia-smi` to fetch utilization and temperature
            result = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=utilization.gpu,temperature.gpu",
                    "--format=csv,noheader,nounits"
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                print(f"Error running nvidia-smi: {result.stderr}")
                return None, None

            # Parse the output (assuming first GPU if multiple GPUs are available)
            lines = result.stdout.strip().split("\n")
            utilization, temperature = map(int, lines[0].split(", "))
            return utilization, temperature

        except Exception as e:
            print(f"Error retrieving GPU stats: {e}")
            return None, None
    
    gpu_util, gpu_temp = get_gpu_utilization_and_temperature()
    cpu_util = get_cpu_utilization()
    memory_util = get_memory_utilization()
    # Return all PC data
    return f"CPU_UTIL:{cpu_util},MEMORY_UTIL:{memory_util},GPU_UTIL:{gpu_util},GPU_TEMP:{gpu_temp}"


def connect(client_name, server_ip, port):
    """Establishes connection to the server."""
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server_ip, port))
            print(f"{client_name} connected to server at {server_ip}:{port}")
            return sock
        except Exception as e:
            print(f"{client_name} failed to connect, retrying... {e}")
            time.sleep(5)


if __name__ == '__main__':
    ip = "192.168.178.63"
    port = 12346
    client_name = "Client B"
    
    # Establish initial connection
    socket_conn = connect(client_name, ip, port)

    while True:
        try:
            print("Sending data...")
            data = get_pc_data()
            socket_conn.sendall(str(data).encode('utf-8'))
            print(f"Data sent: {data}")
            time.sleep(5)  # Send data every 5 seconds
        except Exception as e:
            print(f"{client_name} error: {e}. Reconnecting...")
            time.sleep(5)
            # Create a new connection
            socket_conn = connect(client_name, ip, port)
