#!/bin/bash

USED_SPACE=$(df -BG --output=pcent / | sed -n 2p | tr -d  " " | tr -d "%")

if [[ "$USED_SPACE" -gt 60 ]]; then
    rsync -rltgoDv --remove-source-files /home/pi/Documents/Alarm /storage/Alarm
else
    echo "More then 30% free space" 
fi
