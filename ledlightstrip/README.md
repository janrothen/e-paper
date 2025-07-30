# LED

Raspberry Pi project to control an RGB LED strip based on the time of day using scheduled tasks and systemd services.

### led.py
Turns on the LED strip with a color configured in config.conf.

https://danidudas.medium.com/how-to-connect-rgb-strip-led-lights-to-raspberry-pi-zero-w-and-control-from-node-js-70ddfec19f0b

## Prerequisites
```
python3  
configparser==3.5.0  
python-dateutil==2.7.3  
```
## Installing

Create symlink to utils in this directory, or imports won't work.
Configure the scripts: `config.conf`

Follow the pigpio installation instructions:
```
https://abyz.me.uk/rpi/pigpio/download.html
```
or
`sudo apt-get install pigpio`

### 
```
$ sudo systemctl start pigpiod
```

## Development Setup

### Virtual Environment
Create and activate a virtual environment for development:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install test dependencies
pip install -r requirements-test.txt
```

### Running the Application
The application supports multiple effects via command-line arguments:

```bash
# Basic profile effect (morning/evening colors based on time)
./run.py profile

# Breathing effect with custom color and duration
./run.py breathing --color red --duration 3000

# Random color changes
./run.py random --interval 2000

# Color cycling through multiple colors
./run.py cycle --colors red,green,blue,yellow --duration 2500

# Fade between two colors
./run.py fade --from black --to white --duration 5000

# Use hex colors
./run.py breathing --color "#FF6347"

# Get help
./run.py --help
```

### Running Tests
The project includes comprehensive unit tests with hardware mocking:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=led --cov=config --cov=cli --cov=utils

# Run tests with detailed coverage report (generates HTML)
pytest --cov=led --cov=config --cov=cli --cov=utils --cov-report=html

# Run specific test file
pytest tests/test_color.py

# Run tests matching a pattern
pytest -k "test_color"

# Run tests with verbose output
pytest -v

# Skip slow tests
pytest -m "not slow"
```

### Project Structure
```
ledlightstrip/
├── led/                   # Core LED control modules
│   ├── color.py           # Color management
│   ├── effects.py         # LED effects (breathing, fade, etc.)
│   ├── gpio_service.py    # Hardware GPIO interface
│   ├── ledlightstrip_controller.py # Main LED controller
│   └── profile_manager.py # Time-based color profiles
├── config/                # Configuration management
├── cli/                   # Command-line interface
├── utils/                 # Utilities (logging, shutdown handling)
├── tests/                 # Unit tests with mocked hardware
├── service/               # Systemd service files
└── run.py                 # Main application entry point
```

## Timers

Copy `led.service` to `/etc/systemd/system`

Create a file in `/etc/cron.d/led` to start/stop the systemd service.
```
/etc/cron.d $ cat led  
15 19 * * * root /bin/systemctl start led 2>/tmp/error
30 22 * * * root /bin/systemctl stop led 2>/tmp/error

15 06 * * * root /bin/systemctl start led 2>/tmp/error
30 08 * * * root /bin/systemctl stop led 2>/tmp/error
```

### Status
```
pi@zero:~ $ systemctl status led.service
● led.service - LED Service
     Loaded: loaded (/etc/systemd/system/led.service; disabled; vendor preset: enabled)
     Active: active (running) since Mon 2023-04-10 13:19:34 CEST; 24s ago
   Main PID: 18876 (python3)
      Tasks: 3 (limit: 415)
        CPU: 14.115s
     CGroup: /system.slice/led.service
             ├─18876 /usr/bin/python3 -u led.py
             ├─21052 sh -c pigs p 17 3
             └─21053 pigs p 17 3
```
