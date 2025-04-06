#!/usr/bin/env bash
set -euo pipefail

# list of ports to free up
ports=(5701 5702 5703 5801 5802)

# helper to kill by PID list
kill_pids() {
  local pids=($1)
  if [ ${#pids[@]} -gt 0 ]; then
    echo "Killing PIDs: ${pids[*]}"
    kill "${pids[@]}"
  fi
}

for port in "${ports[@]}"; do
  echo "→ Checking port $port…"
  # try lsof first
  if command -v lsof >/dev/null; then
    pids=$(lsof -t -i tcp:"$port" 2>/dev/null || true)
  else
    # fallback to fuser
    pids=$(fuser "$port"/tcp 2>/dev/null || true)
  fi

  if [ -n "$pids" ]; then
    kill_pids "$pids"
  else
    echo "   no process found on port $port"
  fi
done
