# E-Ink

### run.py
TODO

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
cd ~/raspberry/epaper
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
