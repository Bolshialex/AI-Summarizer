#!/bin/bash
# Launches the backend and frontend in two separate Terminal windows.

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

open_terminal() {
  osascript <<EOF
tell application "Terminal"
  activate
  do script "$1"
end tell
EOF
}

open_terminal "cd '$DIR/backend' && ./run_server.sh"
open_terminal "cd '$DIR/frontend' && npm install && npm run dev"

echo "Backend and frontend are starting in two Terminal windows."
echo "Backend:  http://127.0.0.1:8000"
echo "Frontend: http://localhost:5173"
