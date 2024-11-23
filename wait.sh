#!/usr/bin/env bash
# wait-for-it.sh: A script to wait for a service to be available.
# Usage: ./wait-for-it.sh <host>:<port> -- <command>

TIMEOUT=15
WAIT_TIME=1
HOST=""
PORT=""
CMD=""
RETRIES=5

usage() {
  echo "Usage: $0 <host>:<port> -- <command>"
  exit 1
}

wait_for() {
  local host="$1"
  local port="$2"
  local timeout="$3"
  local wait_time="$4"
  local retries="$5"

  for i in $(seq 1 "$retries"); do
    if nc -z "$host" "$port"; then
      echo "$host:$port is available!"
      return 0
    fi
    echo "Waiting for $host:$port ($i/$retries)..."
    sleep "$wait_time"
  done

  echo "Timeout waiting for $host:$port"
  return 1
}

if [[ $# -lt 2 ]]; then
  usage
fi

HOST=$(echo "$1" | cut -d ':' -f 1)
PORT=$(echo "$1" | cut -d ':' -f 2)
shift

if [[ $# -ge 1 ]]; then
  CMD="$*"
fi

wait_for "$HOST" "$PORT" "$TIMEOUT" "$WAIT_TIME" "$RETRIES"

if [[ -n "$CMD" ]]; then
  exec $CMD
fi