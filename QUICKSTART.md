# RetroTINK Integration - Quick Start Guide

## What You've Got

A complete custom Home Assistant integration for controlling your RetroTINK-4K Pro and CE devices via serial/USB.

## File Structure

```
retrotink_integration/
├── custom_components/
│   └── retrotink/
│       ├── __init__.py           # Integration setup
│       ├── config_flow.py        # UI configuration
│       ├── const.py              # Constants & command mappings
│       ├── manifest.json         # Integration metadata
│       ├── remote.py             # Remote entity implementation
│       ├── services.yaml         # Service definitions
│       ├── strings.json          # UI strings
│       └── translations/
│           └── en.json           # English translations
├── install.sh                    # Installation script
├── README.md                     # Full documentation
├── EXAMPLES.md                   # Example configs & automations
└── UNFOLDED_CIRCLE.md           # Unfolded Circle setup guide
```

## Installation (Choose One Method)

### Method 1: Automated Installation

```bash
cd retrotink_integration
./install.sh /path/to/homeassistant/config
```

Example paths:
- Standard: `/home/homeassistant/.homeassistant`
- Docker/HAOS: `/config`
- Supervised: `/usr/share/hassio/homeassistant`

### Method 2: Manual Installation

```bash
# Copy the integration folder
cp -r custom_components/retrotink /path/to/homeassistant/config/custom_components/

# Restart Home Assistant
```

### Method 3: Via File Upload (Home Assistant OS)

1. Use the File Editor add-on or Samba share
2. Navigate to the `config` directory
3. Create `custom_components/retrotink/` folder
4. Upload all files from `custom_components/retrotink/` to that folder

## Initial Setup

### 1. Set Serial Port Permissions

Your Home Assistant needs permission to access the USB serial ports:

```bash
# Add homeassistant user to dialout group
sudo usermod -a -G dialout homeassistant

# Or set permissions directly
sudo chmod 666 /dev/ttyUSB0
sudo chmod 666 /dev/ttyUSB1
```

### 2. Restart Home Assistant

After installation, restart Home Assistant completely.

### 3. Add Integration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "RetroTINK Serial Remote"
4. Configure first device:
   - Name: "RetroTINK 4K Pro"
   - Serial Port: `/dev/ttyUSB0`
5. Click Submit
6. Repeat for second device:
   - Name: "RetroTINK 4K CE"
   - Serial Port: `/dev/ttyUSB1`

### 4. Test It

Go to **Developer Tools** → **Services** and try:

```yaml
service: remote.send_command
target:
  entity_id: remote.retrotink_4k_pro
data:
  command: menu
```

If the menu appears on your RetroTINK, you're all set!

## Quick Command Reference

```yaml
# Single command
service: remote.send_command
data:
  command: menu

# Multiple commands with delay
service: remote.send_command
data:
  command:
    - menu
    - down
    - enter
  delay_secs: 0.5

# Repeat command
service: remote.send_command
data:
  command: up
  num_repeats: 3
```

## Common Commands

**Navigation:** `menu`, `up`, `down`, `left`, `right`, `ok`, `back`

**Functions:** `input`, `output`, `scaler`, `sfx`, `adc`, `col`, `aud`

**Profiles:** `prof` (menu), `prof1` - `prof12` (direct access)

**Resolution:** `res4k`, `res1080p`, `res1440p`, `res480p`

**Auto:** `gain`, `phase`

**Special:** `pause`, `safe`, `genlock`, `buffer`

**Power:** `power_on`, `power_off`

**See [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md) for the complete list of 70+ commands.**

## Unfolded Circle Setup

See `UNFOLDED_CIRCLE.md` for detailed instructions on integrating with your Unfolded Circle Remote 3.

**Quick version:**
1. Ensure integration is working in Home Assistant
2. Open Unfolded Circle app
3. Your RetroTINK remotes should appear automatically
4. Add them to an activity and map buttons

## Troubleshooting

**Integration doesn't appear:**
- Make sure you restarted HA after copying files
- Check logs: Settings → System → Logs

**Can't connect during setup:**
- Verify serial port path: `ls -l /dev/ttyUSB*`
- Check permissions: `sudo chmod 666 /dev/ttyUSB0`
- Make sure RetroTINK is powered on and connected

**Commands not working:**
- Test serial directly: `echo "remote menu" > /dev/ttyUSB0`
- Check entity state in Developer Tools
- Enable debug logging (see README.md)

**On Unfolded Circle:**
- Verify entities show as "available" in Home Assistant
- Restart Unfolded Circle integration
- Test commands in HA first before using remote

## Next Steps

1. **Read the full documentation**: See `README.md`
2. **Check out examples**: See `EXAMPLES.md` for automations and Lovelace cards
3. **Set up Unfolded Circle**: See `UNFOLDED_CIRCLE.md`
4. **Create automations**: Automate profile switching, power management, etc.

## Getting Help

1. Check Home Assistant logs for errors
2. Enable debug logging (instructions in README.md)
3. Test commands using Developer Tools
4. Verify serial connections and permissions

## Credits

Integration created for RetroTINK-4K Pro and CE devices.
RetroTINK is a trademark of RetroTINK LLC.

---

**You're ready to go! Enjoy seamless control of your RetroTINK devices through Home Assistant and Unfolded Circle Remote 3.**
