#!/bin/bash

# Open a new xterm and run npm run serve
xterm -e "cd ./sara/sara/SARA-timothy/frontend && npm run serve" &

# Wait for a moment to ensure the frontend server is up
sleep 10

# activate virtual environment
source ./sara/sara/.venv/bin/activate

#ensure DISPLAY is set
export DISPLAY=0.0

#run the script in xterm
xterm -hold -e "python -u ./sara/sara/SARA-timothy/backend/main.py" .

# Wait for a moment to ensure the server is up
sleep 5

# Open a browser and navigate to localhost:8080 and localhost:5000
xdg-open http://127.0.0.1:5000
xdg-open http://127.0.0.1:8080