# LED Service Installation Guide

## Overview
This systemd service runs the LED strip light controller application as a background daemon on your Raspberry Pi.

## Prerequisites
- Raspberry Pi with Raspberry Pi OS
- Python 3.x installed
- pigpio daemon installed and running
- LED strip light application files in `/home/pi/raspberry/ledstriplight/`

## Installation steps

### 1. Install the service file
Copy the service file to the systemd directory:
```bash
sudo cp ledstriplight.service /etc/systemd/system/
```

### 2. Set proper permissions
```bash
sudo chmod 644 /etc/systemd/system/ledstriplight.service
```

### 3. Reload systemd
Tell systemd to reload its configuration:
```bash
sudo systemctl daemon-reload
```

### 4. Enable the service
Enable the service to start automatically on boot:
```bash
sudo systemctl enable ledstriplight.service
```

### 5. Start the service
Start the service immediately:
```bash
sudo systemctl start ledstriplight.service
```

### 6. Automated scheduling
Define when the service should start and stop—every day, only on weekdays
Copy `ledstriplight` to `/etc/cron.d/`
```bash
sudo cp ledstriplight /etc/cron.d/
sudo chmod 644 /etc/cron.d/ledstriplight
```

## Service management commands

| Command | Description |
|---------|-------------|
| `sudo systemctl start ledstriplight.service` | Start the service |
| `sudo systemctl stop ledstriplight.service` | Stop the service |
| `sudo systemctl restart ledstriplight.service` | Restart the service |
| `sudo systemctl status ledstriplight.service` | Check service status |
| `sudo systemctl enable ledstriplight.service` | Enable auto-start on boot |
| `sudo systemctl disable ledstriplight.service` | Disable auto-start on boot |

## Monitoring and troubleshooting

### View service status
```bash
sudo systemctl status ledstriplight.service
```

### View live logs
```bash
sudo journalctl -u ledstriplight.service -f
```

### View recent logs
```bash
sudo journalctl -u ledstriplight.service --since "1 hour ago"
```

### View all logs
```bash
sudo journalctl -u ledstriplight.service --no-pager
```

## Configuration notes

- **Working directory**: The service runs from `/home/pi/raspberry/ledstriplight/`
- **User**: Runs as the `pi` user (not root for security)
- **Auto-restart**: The service will automatically restart if it crashes
- **Dependencies**: Waits for network and pigpio daemon to be ready
- **Graceful shutdown**: Uses SIGTERM for clean shutdown with 30-second timeout

## Troubleshooting

### Service won't start
1. Check if the working directory exists: `ls -la /home/pi/raspberry/ledstriplight/`
2. Check if `run.py` is executable: `ls -la /home/pi/raspberry/led/run.py`
3. Verify pigpio is running: `sudo systemctl status pigpiod`
4. Check for Python errors: `sudo journalctl -u ledstriplight.service`

### Permission issues
If you get permission errors, ensure:
- The `pi` user owns the application files: `sudo chown -R pi:pi /home/pi/raspberry/ledstriplight/`
- The `pi` user is in the `gpio` group: `sudo usermod -a -G gpio pi`

### Service keeps restarting
Check the logs for errors:
```bash
sudo journalctl -u ledstriplight.service --since "10 minutes ago"
```

## Uninstalling

To remove the service:
```bash
sudo systemctl stop ledstriplight.service
sudo systemctl disable ledstriplight.service
sudo rm /etc/systemd/system/ledstriplight.service
sudo systemctl daemon-reload
```