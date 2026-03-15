#!/bin/bash
set -e

echo "DISPLAY is: $DISPLAY"
echo "XAUTHORITY is: $XAUTHORITY"

# Grant access
xhost +si:localuser:root 2>/dev/null || xhost +local: 2>/dev/null || xhost +

# Build xauth file
XAUTH=/tmp/.docker.xauth
touch $XAUTH
chmod 777 $XAUTH

if xauth nlist $DISPLAY 2>/dev/null | grep -q .; then
  xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $XAUTH nmerge -
  echo "xauth cookie written"
else
  echo "No xauth entries found, copying XAUTHORITY directly"
  cp $XAUTHORITY $XAUTH 2>/dev/null || echo "Warning: could not copy XAUTHORITY"
fi

export XAUTHORITY=$XAUTH

docker compose -f compose.gui.yaml up
