# RetroTINK-4K Serial Remote Integration for Home Assistant

A custom Home Assistant integration for controlling RetroTINK-4K devices (Pro and CE models) via serial over USB.

## Features

- Full remote control of RetroTINK-4K Pro and CE devices
- Exposes devices as Home Assistant remote entities
- Multiple device support - add both Pro and CE (or multiple units)
- Device model selection (Pro or CE) with proper device identification
- UI-based configuration flow
- Standard remote command mapping (up, down, left, right, enter, menu, etc.)
- Direct RetroTINK-4K command support

## Installation

### HACS

1. Open HACS in Home Assistant
2. Go to Integrations
3. Click the three dots in the top right and select "Custom repositories"
4. Add this repository URL and select "Integration" as the category
5. Click "Install"
6. Restart Home Assistant

### Manual Installation

1. Copy the entire `custom_components/retrotink` directory to your Home Assistant's `config/custom_components/` directory
2. Restart Home Assistant
3. The integration should now be available

## Configuration

### Finding Your Serial Ports

First, identify which USB ports your RetroTINK devices are connected to:

```bash
ls -l /dev/ttyUSB*
```

You should see devices like `/dev/ttyUSB0` and `/dev/ttyUSB1`.

### Setting Up the Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "RetroTINK-4K Serial Remote Control"
4. Follow the configuration flow:
   - Enter a name for your device (e.g., "Living Room RetroTINK Pro")
   - Select the device model (RetroTINK-4K Pro or RetroTINK-4K CE)
   - Enter the serial port (e.g., `/dev/ttyUSB0`)
5. Repeat for your second device if you have both Pro and CE

### Permissions

Ensure Home Assistant has permission to access the serial ports:

```bash
sudo usermod -a -G dialout homeassistant
sudo chmod 666 /dev/ttyUSB0
sudo chmod 666 /dev/ttyUSB1
```

For persistent permissions, create a udev rule:

```bash
sudo nano /etc/udev/rules.d/99-retrotink.rules
```

Add:
```
SUBSYSTEM=="tty", ATTRS{idVendor}=="YOUR_VENDOR_ID", ATTRS{idProduct}=="YOUR_PRODUCT_ID", MODE="0666"
```

Then reload:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

## Usage

### Basic Commands

Once configured, you'll have remote entities for each device. You can control them via:

**Home Assistant UI:**
- Navigate to the device in Settings → Devices & Services
- Use the remote control interface

**Services:**

```yaml
# Send a single command
service: remote.send_command
target:
  entity_id: remote.retrotink_4k_pro
data:
  command: menu

# Send multiple commands
service: remote.send_command
target:
  entity_id: remote.retrotink_4k_pro
data:
  command:
    - menu
    - down
    - down
    - enter

# Send with repeats
service: remote.send_command
target:
  entity_id: remote.retrotink_4k_pro
data:
  command: up
  num_repeats: 3
  delay_secs: 0.4
```

### Supported Commands

The integration supports all RetroTINK-4K commands. See [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md) for the complete list.

For detailed command documentation, visit the official wiki:  
**[RetroTINK-4K Remote Control Commands](https://consolemods.org/wiki/AV:RetroTINK-4K#Remote_Control_Commands)**

**Key Commands:**

**Navigation:**  
`menu`, `up`, `down`, `left`, `right`, `ok`, `back`

**Profiles:**  
`prof`, `prof1` - `prof12`

**Resolution:**  
`res4k`, `res1080p`, `res1440p`, `res480p`

**Main Functions:**  
`input`, `output`, `scaler`, `sfx`, `adc`, `col`, `aud`

**Auto Functions:**  
`gain`, `phase`

**Special:**  
`pause`, `safe`, `genlock`, `buffer`

**Auxiliary:**  
`aux1` - `aux8`

**Power:**  
`pwr on` (turn on), `pwr` (turn off)

You can send raw RetroTINK commands directly - they'll automatically be prefixed with "remote".

### Automations

You can create automations to control your RetroTINK devices:

```yaml
automation:
  - alias: "Switch RetroTINK Profile on Input Change"
    trigger:
      platform: state
      entity_id: input_select.gaming_console
    action:
      - service: remote.send_command
        target:
          entity_id: remote.retrotink_4k_pro
        data:
          command: "prof"
```

## Troubleshooting

### Device Not Responding

1. Check serial port permissions
2. Verify the correct port is configured
3. Try disconnecting and reconnecting the USB cable
4. Check Home Assistant logs for error messages

### Commands Not Working

1. Verify the RetroTINK device is powered on
2. Check that you're using valid command names
3. Increase the `delay_secs` if sending multiple commands rapidly
4. Enable debug logging (see below)

### Debug Logging

Add to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.retrotink: debug
```

## Technical Details

- **Communication:** Serial over USB at 115200 baud (8N1: 8 data bits, no parity, 1 stop bit)
- **Serial Configuration:** Automatically configured using `stty -F <port> 115200 cs8 -cstopb -parenb`
- **Command Format:** `remote <command>\n` (all commands get this prefix)
- **Power Commands:** 
  - Power On: `pwr on\n` (ONLY command without "remote" prefix)
  - Power Off: `remote pwr\n` (gets "remote" prefix like other commands)
- **Connection:** Opens/closes serial connection for each command (prevents blocking)
- **Entity Type:** RemoteEntity (standard Home Assistant remote platform)
- **Power State:** Tracked locally based on power commands sent (device doesn't report state)
- **Command List:** All 70+ RetroTINK commands supported (see COMMAND_REFERENCE.md)

## Credits

Created for use with RetroTINK-4K Pro and CE devices manufactured by RetroTINK LLC.

**Special thanks to Mike Chi** (@retrotink2) for creating the RetroTINK line of products and making the world of retro gaming better for everyone.

### Links
- **Purchase RetroTINK Products**: https://www.retrotink.com
- **Follow Mike Chi on X/Twitter**: https://www.x.com/retrotink2
- **Command Documentation**: https://consolemods.org/wiki/AV:RetroTINK-4K#Remote_Control_Commands

## License

MIT License - Feel free to modify and distribute as needed.

## Support

For issues or feature requests, please open an issue on the GitHub repository.
