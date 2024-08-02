#!/bin/bash

echo "Worker Initiated"

echo "Starting SD API Server For PROD 🚀"
python server_fastapi.py &

echo "Starting RunPod Handler 🏃‍♂💨"

python -u ./runpod_handler.py