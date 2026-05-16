#!/bin/bash

# Usage: ./delete-wing-drawers.sh <wing_name>
# Deletes all drawers from the specified MemPalace wing recursively

set -e

if [ -z "$1" ]; then
  echo "Error: Wing name is required"
  echo "Usage: $0 <wing_name>"
  exit 1
fi

WING="$1"
LIMIT=50

echo "Deleting all drawers from wing: $WING"

while true; do
  # List drawers for the wing
  RESPONSE=$(opencode mcp call mempalace mempalace_list_drawers --wing "$WING" --limit "$LIMIT" 2>/dev/null || true)
  
  if [ -z "$RESPONSE" ]; then
    echo "No more drawers found or failed to list drawers"
    break
  fi
  
  # Extract drawer IDs
  DRAWER_IDS=$(echo "$RESPONSE" | jq -r '.drawers[].drawer_id' 2>/dev/null || true)
  
  if [ -z "$DRAWER_IDS" ]; then
    echo "No drawers found in wing: $WING"
    break
  fi
  
  # Delete each drawer
  for DRAWER_ID in $DRAWER_IDS; do
    echo "Deleting drawer: $DRAWER_ID"
    opencode mcp call mempalace mempalace_delete_drawer --drawer_id "$DRAWER_ID" >/dev/null 2>&1 || true
  done
done

echo "Finished deleting drawers from wing: $WING"
