# RetroTINK-4K Command Reference

This integration supports all RetroTINK-4K serial commands.

## Official Documentation

For complete command documentation and explanations of what each command does, see:  
**[RetroTINK-4K Remote Control Commands](https://consolemods.org/wiki/AV:RetroTINK-4K#Remote_Control_Commands)**

## Command Format

All commands (except `pwr on`) are automatically prefixed with `remote` when sent to the device.

**Example:**
- You send: `menu`
- Device receives: `remote menu`

## Power Commands

| Command | Raw Command Sent | Has 'remote' Prefix? |
|---------|------------------|---------------------|
| `pwr on` | `pwr on` | **NO** - Only command without prefix |
| `pwr` | `remote pwr` | **YES** - Gets prefix |

## Available Commands

Use these exact command names when calling `remote.send_command`:

### Navigation
`menu`, `up`, `down`, `left`, `right`, `ok`, `back`

### Information
`diag`, `stat`

### Main Functions
`input`, `output`, `scaler`, `sfx`, `adc`, `col`, `aud`

### Profiles
`prof`, `prof1`, `prof2`, `prof3`, `prof4`, `prof5`, `prof6`, `prof7`, `prof8`, `prof9`, `prof10`, `prof11`, `prof12`

### Auto Functions
`gain`, `phase`

### Special Functions
`pause`, `safe`, `genlock`, `buffer`

### Resolution Presets
`res4k`, `res1080p`, `res1440p`, `res480p`, `res1`, `res2`, `res3`, `res4`

### Auxiliary Functions
`aux1`, `aux2`, `aux3`, `aux4`, `aux5`, `aux6`, `aux7`, `aux8`

## Usage Examples

### Single Command
```yaml
service: remote.send_command
target:
  entity_id: remote.retrotink_4k_pro
data:
  command: menu
```

### Multiple Commands
```yaml
service: remote.send_command
target:
  entity_id: remote.retrotink_4k_pro
data:
  command:
    - menu
    - down
    - ok
  delay_secs: 0.5
```

### Load Profile
```yaml
service: remote.send_command
target:
  entity_id: remote.retrotink_4k_pro
data:
  command: prof3
```

### Power Control
```yaml
# Turn on
service: remote.turn_on
target:
  entity_id: remote.retrotink_4k_pro

# Turn off
service: remote.turn_off
target:
  entity_id: remote.retrotink_4k_pro
```

## Learn More

- **Command Details**: https://consolemods.org/wiki/AV:RetroTINK-4K#Remote_Control_Commands
- **Purchase RetroTINK**: https://www.retrotink.com
- **Follow Mike Chi**: https://www.x.com/retrotink2
