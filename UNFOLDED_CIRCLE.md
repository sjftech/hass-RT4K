# Unfolded Circle Remote 3 Setup Guide

This guide will help you integrate your RetroTINK devices with the Unfolded Circle Remote 3.

## Prerequisites

1. RetroTINK integration installed and configured in Home Assistant
2. Unfolded Circle Remote 3 integration set up in Home Assistant
3. Both RetroTINK devices configured and working (test with HA first)

## Configuration Steps

### 1. Verify Home Assistant Integration

1. Open Home Assistant
2. Go to **Settings** → **Devices & Services**
3. Verify you see the **Unfolded Circle** integration
4. Verify you see your **RetroTINK Serial Remote** devices

### 2. Check Remote Entities

1. Go to **Developer Tools** → **States**
2. Search for `remote.retrotink`
3. You should see both entities:
   - `remote.retrotink_4k_pro`
   - `remote.retrotink_4k_ce`

### 3. Configure in Unfolded Circle App

1. Open the Unfolded Circle Remote app
2. Go to **Devices** or **Configuration**
3. Your RetroTINK remotes should appear automatically under Home Assistant devices
4. Add them to an activity
5. Map buttons to commands using "Send Command" feature
6. Use command names from the list below

#### Available Commands
All commands use the format shown in [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md):
- **Navigation**: menu, up, down, left, right, ok, back
- **Profiles**: prof, prof1-prof12
- **Resolution**: res4k, res1080p, res1440p, res480p, res1-res4
- **Main Functions**: input, output, scaler, sfx, adc, col, aud
- **Auto**: gain, phase
- **Special**: pause, safe, genlock, buffer
- **Auxiliary**: aux1-aux8
- **Power**: power_on, power_off

### 4. Button Mapping

Map your Unfolded Circle buttons to these commands:

#### Basic Navigation
- **D-Pad Up** → `up`
- **D-Pad Down** → `down`
- **D-Pad Left** → `left`
- **D-Pad Right** → `right`
- **OK/Enter** → `enter`
- **Back** → `back`

#### Special Functions
- **Menu** → `menu`
- **Red Button** → `prof` (Profile)
- **Green Button** → `output` (Output)
- **Yellow Button** → `status` (Status)
- **Blue Button** → `safe` (Safe Mode)

#### Power
- **Power** → `power`

### 5. Creating Activities

#### Example: Retro Gaming Activity

**Devices:**
- RetroTINK-4K Pro
- Your TV
- Your Audio Receiver

**Power On Sequence:**
```yaml
1. Turn on TV
2. Turn on Audio Receiver
3. Switch TV to HDMI input
4. Send "output" to RetroTINK (to verify output)
```

**Power Off Sequence:**
```yaml
1. Turn off RetroTINK
2. Turn off Audio Receiver
3. Turn off TV
```

#### Example: Multiple Consoles

If you have both Pro and CE for different consoles:

**Activity: SNES Gaming**
- Device: RetroTINK-4K Pro
- Profile: SNES optimized

**Activity: PlayStation Gaming**
- Device: RetroTINK-4K CE
- Profile: PlayStation optimized

### 6. Advanced: Macro Commands

You can create macros in the Unfolded Circle app to send multiple commands:

#### Quick Profile Switch Macro
```
Command: prof
Delay: 500ms
Command: down
Delay: 500ms
Command: enter
```

#### Navigate to Scaling Menu Macro
```
Command: menu
Delay: 400ms
Command: right
Delay: 400ms
Command: enter
```

## Troubleshooting

### RetroTINK Devices Not Appearing

1. Check Home Assistant is properly connected to Unfolded Circle
2. Restart the Unfolded Circle integration in Home Assistant
3. Restart the Unfolded Circle Remote
4. Ensure the RetroTINK entities are showing as available in HA

### Commands Not Working

1. Test commands directly in Home Assistant first
2. Check serial port permissions on your Home Assistant host
3. Verify the correct serial ports are configured
4. Try increasing the delay between commands in macros

### Delays Between Commands

If commands are being sent too quickly:
1. In Unfolded Circle, adjust the delay between macro steps
2. In Home Assistant automations, use the `delay_secs` parameter:
```yaml
service: remote.send_command
target:
  entity_id: remote.retrotink_4k_pro
data:
  command:
    - menu
    - down
    - enter
  delay_secs: 0.5
```

## Recommended Button Layout

### Page 1: Navigation
```
┌─────────┬─────────┬─────────┐
│  Menu   │   Up    │  Back   │
├─────────┼─────────┼─────────┤
│  Left   │   OK    │  Right  │
├─────────┼─────────┼─────────┤
│ Profile │  Down   │ Output  │
└─────────┴─────────┴─────────┘
```

### Page 2: Quick Functions
```
┌─────────┬─────────┬─────────┐
│ Status  │  Auto   │  Phase  │
├─────────┼─────────┼─────────┤
│ Input   │  Safe   │ Ch Up   │
├─────────┼─────────┼─────────┤
│  Mute   │ Vol Up  │ Ch Down │
└─────────┴─────────┴─────────┘
```

## Tips

1. **Test First**: Always test commands in Home Assistant before configuring in Unfolded Circle
2. **Use Delays**: RetroTINK devices need small delays between commands (~400ms)
3. **Create Macros**: Use macros for common multi-step operations
4. **Label Buttons**: Use clear labels so you remember what each button does
5. **Backup Config**: Export your Unfolded Circle configuration after setup

## Support

If you encounter issues:
1. Check Home Assistant logs: **Settings** → **System** → **Logs**
2. Enable debug logging for the RetroTINK integration
3. Test commands using Developer Tools in Home Assistant
4. Check the Unfolded Circle community forums

## Example Complete Configuration

Here's a complete example of a well-configured activity:

**Activity Name:** Retro Gaming Setup

**Devices:**
- remote.retrotink_4k_pro
- remote.retrotink_4k_ce
- media_player.living_room_tv
- media_player.av_receiver

**Button Mappings:**
- Navigation: Standard D-pad + OK + Back
- Function 1: Profile Switch
- Function 2: Output Mode
- Function 3: Safe Mode
- Function 4: Status Display

**Startup Macro:**
```
1. Power on TV (2 sec delay)
2. Power on AV Receiver (2 sec delay)
3. Select HDMI input on TV (1 sec delay)
4. Send "output" to RetroTINK Pro
```

This provides a seamless experience when starting your retro gaming session!
