"""Constants for the RetroTINK Serial Remote integration."""

DOMAIN = "retrotink"

CONF_SERIAL_PORT = "serial_port"
CONF_DEVICE_MODEL = "device_model"

DEVICE_MODELS = {
    "RetroTINK-4K Pro": "RetroTINK-4K Pro",
    "RetroTINK-4K CE": "RetroTINK-4K CE",
}

# Complete mapping of button names to RetroTINK serial commands
# All commands will be prefixed with "remote" when sent
COMMAND_MAP = {
    # Navigation
    "menu": "menu",
    "up": "up",
    "down": "down",
    "left": "left",
    "right": "right",
    "ok": "ok",
    "enter": "ok",  # Alias for ok
    "back": "back",
    
    # Information/Diagnostics
    "diagnostics": "diag",
    "diag": "diag",
    "statistics": "stat",
    "stat": "stat",
    
    # Main Functions
    "input": "input",
    "output": "output",
    "scaler": "scaler",
    "cropping": "scaler",  # Alias
    "processing": "sfx",
    "effects": "sfx",
    "sfx": "sfx",
    "adc": "adc",
    "color": "col",
    "col": "col",
    "audio": "aud",
    "aud": "aud",
    
    # Profiles
    "profiles": "prof",
    "prof": "prof",
    "profile1": "prof1",
    "prof1": "prof1",
    "profile2": "prof2",
    "prof2": "prof2",
    "profile3": "prof3",
    "prof3": "prof3",
    "profile4": "prof4",
    "prof4": "prof4",
    "profile5": "prof5",
    "prof5": "prof5",
    "profile6": "prof6",
    "prof6": "prof6",
    "profile7": "prof7",
    "prof7": "prof7",
    "profile8": "prof8",
    "prof8": "prof8",
    "profile9": "prof9",
    "prof9": "prof9",
    "profile10": "prof10",
    "prof10": "prof10",
    "profile11": "prof11",
    "prof11": "prof11",
    "profile12": "prof12",
    "prof12": "prof12",
    
    # Auto Functions
    "gain": "gain",
    "auto_gain": "gain",
    "phase": "phase",
    "auto_phase": "phase",
    
    # Special Functions
    "pause": "pause",
    "safe": "safe",
    "safe_mode": "safe",
    "genlock": "genlock",
    "gen_lock": "genlock",
    "buffer": "buffer",
    "triple_buffer": "buffer",
    
    # Resolution Presets
    "4k": "res4k",
    "res4k": "res4k",
    "1080p": "res1080p",
    "res1080p": "res1080p",
    "1440p": "res1440p",
    "res1440p": "res1440p",
    "480p": "res480p",
    "res480p": "res480p",
    "res1": "res1",
    "custom1": "res1",
    "res2": "res2",
    "custom2": "res2",
    "res3": "res3",
    "custom3": "res3",
    "res4": "res4",
    "custom4": "res4",
    
    # Auxiliary Functions
    "aux1": "aux1",
    "auto_crop_vertical": "aux1",
    "aux2": "aux2",
    "auto_crop_4_3": "aux2",
    "aux3": "aux3",
    "auto_crop_16_9": "aux3",
    "aux4": "aux4",
    "aux5": "aux5",
    "aux6": "aux6",
    "aux7": "aux7",
    "aux8": "aux8",
}

# Power commands (special handling)
POWER_ON_CMD = "pwr on"  # Only command without "remote" prefix
POWER_OFF_CMD = "pwr"     # This will get "remote" prefix added
