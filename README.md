# E-Paper Bitcoin Price Ticker

An e-paper Bitcoin price ticker that displays the current price of Bitcoin using a Waveshare e-ink display on a Raspberry Pi 5.

## Prerequisites
```
python3
python3-pip
```
Other requirements will be installed from [requirements.txt](requirements.txt).

## Installing
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Start In Background (survives logout)
```bash
cd ~/raspberry
source .venv/bin/activate
nohup python run.py >/tmp/epaper.log 2>&1 &
```

Check logs:
```bash
tail -f /tmp/epaper.log
```

Stop:
```bash
pkill -f "python run.py"
```
