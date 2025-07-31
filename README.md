# PlantHumidity

A personal project to monitor the humidity of my own plants soil using sensors, with local network API integration.

## Purpose

This repository is for my own use, to track and log the humidity levels of my plants soil. It collects data from humidity sensors and helps me keep my plants healthy by showing me when water is needed. The project also includes an API integration for accessing humidity data and controlling sensors over my local network.

## Features

- Read humidity levels from connected sensors
- Log data for historical tracking
- Simple scripts for data collection and monitoring
- Local network API integration for remote access and automation
- Local network API for CRUD

## Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/DavidWaligora/PlantHumidity.git
   cd PlantHumidity
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Connect your humidity sensor** and update configuration files/scripts as needed.

## Usage

Run the main script to start monitoring:
```bash
python main.py
```

Check the log files for humidity records and alerts.

### Local Network API

The project provides an API to access sensor data and automate plant care via devices on your local network.  
See the `api/` directory or API documentation for details on available endpoints and usage.

## Notes

- This project is custom-built for my own plants and sensors.
- No guarantee it will work for other setups.
- Feel free to fork and adapt if you find it useful.

## Technologies Used

- **Python:** Main programming language for scripts and API.
- **Raspberry Pi Zero 2 W:** Hardware platform for running the project and connecting sensors.
- **Soil Humidity Sensors:** Hardware for measuring soil moisture.
- **SQLite:** Database for logging and storing sensor data.
- **Flask:** Framework for local network API integration.

## License

MIT License

---

**Created and maintained by David Waligora**
