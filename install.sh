#!/bin/bash

# RetroTINK Integration Installation Script
# This script copies the integration to your Home Assistant custom_components directory

set -e

echo "RetroTINK Serial Remote Integration Installer"
echo "=============================================="
echo

# Check if HA config directory is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <path-to-home-assistant-config>"
    echo "Example: $0 /home/homeassistant/.homeassistant"
    echo
    echo "Or if using Docker/Home Assistant OS:"
    echo "Example: $0 /config"
    exit 1
fi

HA_CONFIG="$1"

# Verify directory exists
if [ ! -d "$HA_CONFIG" ]; then
    echo "Error: Directory $HA_CONFIG does not exist"
    exit 1
fi

# Create custom_components directory if it doesn't exist
CUSTOM_DIR="$HA_CONFIG/custom_components"
if [ ! -d "$CUSTOM_DIR" ]; then
    echo "Creating custom_components directory..."
    mkdir -p "$CUSTOM_DIR"
fi

# Copy the integration
DEST_DIR="$CUSTOM_DIR/retrotink"
echo "Installing RetroTINK integration to $DEST_DIR..."

# Remove old installation if exists
if [ -d "$DEST_DIR" ]; then
    echo "Removing existing installation..."
    rm -rf "$DEST_DIR"
fi

# Copy files
cp -r custom_components/retrotink "$CUSTOM_DIR/"

echo
echo "Installation complete!"
echo
echo "Next steps:"
echo "1. Restart Home Assistant"
echo "2. Go to Settings → Devices & Services"
echo "3. Click '+ Add Integration'"
echo "4. Search for 'RetroTINK Serial Remote'"
echo "5. Configure your devices:"
echo "   - RetroTINK-4K Pro on /dev/ttyUSB0"
echo "   - RetroTINK-4K CE on /dev/ttyUSB1"
echo
echo "Don't forget to set serial port permissions!"
echo "Run: sudo usermod -a -G dialout homeassistant"
echo "Or: sudo chmod 666 /dev/ttyUSB0 /dev/ttyUSB1"
echo
