#!/bin/bash
# url-helmet.sh

cd /home/angelmurillo/IoT-5

source /home/angelmurillo/IoT-5/venv/bin/activate

uvicorn OpenCV:app --host 0.0.0.0 --port 8000 &
sleep 5  

/home/angelmurillo/.nvm/versions/node/v21.7.3/bin/lt --port 8000 --subdomain ihelmet-octavio

