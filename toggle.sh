#!/bin/bash 

# Navigate to the directory
cd ~/Desktop/Trabajos/Sistemas/IA/Virtual_Asistant

# Check if the script is already running
if pgrep -f always.py > /dev/null
then
    # If the script is running, kill it
    pkill -f always.py
    
else
    # If the script is not running, start it
    ./venv/bin/python always.py
    echo "Started always.py"

fi