#!/bin/bash
# Smart City Traffic AI - EC2 24/7 Web Dashboard Service Setup
set -e

echo "=================================================="
echo "DEPLOYING SMART CITY CONTROL ROOM DASHBOARD ON EC2"
echo "=================================================="

TARGET_DIR="$HOME/smart-city-traffic-ai"

if [ ! -d "$TARGET_DIR" ]; then
    echo "Cloning GitHub repository to $TARGET_DIR..."
    git clone https://github.com/Pawandubey11/smart-city-traffic-ai.git "$TARGET_DIR"
else
    echo "Updating existing repository at $TARGET_DIR..."
    cd "$TARGET_DIR"
    git pull origin main
fi

cd "$TARGET_DIR/frontend"

# Kill any existing server process on port 3000
echo "Cleaning up existing process on port 3000..."
fuser -k 3000/tcp || true
pkill -f "python3 -m http.server 3000" || true

# Start background web server on 0.0.0.0:3000
echo "Starting 24/7 Background Web Server on Port 3000..."
nohup python3 -m http.server 3000 > "$HOME/dashboard.log" 2>&1 &

sleep 2

echo "=================================================="
echo "✅ DEPLOYMENT COMPLETED SUCCESSFULLY!"
echo "Dashboard is now live 24/7 on Port 3000!"
echo "=================================================="
