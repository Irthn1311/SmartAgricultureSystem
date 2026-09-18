# Smart Agriculture System

An academic **IoT + Machine Learning** prototype for monitoring environmental conditions and supporting smart irrigation through an ESP32-connected desktop application.

## Overview

The project combines three layers:

```text
Sensors / ESP32
      |
      | Serial data
      v
Python data pipeline
      |
      +---- PostgreSQL sensor storage
      |
      +---- TensorFlow weather / condition model
      |
      v
PyQt5 desktop application
      |
      +---- environmental dashboard
      +---- manual watering controls
      +---- scheduled / automatic watering
      +---- multilingual UI
```

## Main components

- **ESP32 / Arduino firmware** for sensor and actuator communication
- **Serial reader** for ingesting temperature, humidity, light, and device status
- **PyQt5 desktop UI** for monitoring and control
- **TensorFlow model** and saved scaler for model inference
- **PostgreSQL-oriented sensor storage**
- **Manual and scheduled watering workflows**
- **Vietnamese / English interface support**

## Tech stack

| Area | Technology |
| --- | --- |
| Embedded / IoT | ESP32 / Arduino |
| Application | Python, PyQt5 |
| Machine Learning | TensorFlow / Keras, scikit-learn |
| Data | pandas, NumPy |
| Database | PostgreSQL-oriented integration |
| Device communication | Serial |

## Repository structure

```text
SmartAgricultureSystem/
├── Do_an_model_test.ino          ESP32 / Arduino firmware
├── appPyQt.py                    desktop application
├── serial_reader.py              serial sensor ingestion
├── weather_model.keras           trained model artifact
├── best_model.h5                 model artifact
├── scaler.save                   preprocessing scaler
├── sensor_data_23_27_april_2025.csv
├── data.sql                      database-related script/data
├── pin_config.json               example pin configuration
├── requirements.txt
└── README.md
```

## Local setup

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

The application expects local hardware / database configuration that matches the development environment. Update serial-port, database, and device settings before running it on another machine.

## Security note

Local credentials and user-generated account files should **not** be committed to Git. This repository keeps only example configuration; machine-specific user data belongs in ignored local files.

## Status

This repository is preserved as a portfolio example of integrating embedded devices, sensor data, a desktop UI, a relational database workflow, and a small machine-learning component in one system.

It is an academic prototype rather than a production authentication or deployment reference.
