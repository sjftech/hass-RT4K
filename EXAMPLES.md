# Example Automations and Scripts for RetroTINK Integration

## Example automation.yaml entries

# Quick access to a specific profile
automation:
  - alias: "RetroTINK: Load SNES Profile"
    trigger:
      platform: event
      event_type: retrotink_shortcut
      event_data:
        action: load_snes_profile
    action:
      - service: remote.send_command
        target:
          entity_id: remote.retrotink_4k_pro
        data:
          command: prof2
          
  # Navigate to output settings
  - alias: "RetroTINK: Quick Access to Output Settings"
    trigger:
      platform: event
      event_type: retrotink_shortcut
      event_data:
        action: output_settings
    action:
      - service: remote.send_command
        target:
          entity_id: remote.retrotink_4k_pro
        data:
          command: output

  # Auto-switch resolution based on input
  - alias: "RetroTINK: Auto 4K for Modern Consoles"
    trigger:
      platform: state
      entity_id: input_select.current_console
    action:
      - choose:
          - conditions:
              - condition: state
                entity_id: input_select.current_console
                state: "PS5"
            sequence:
              - service: remote.send_command
                target:
                  entity_id: remote.retrotink_4k_pro
                data:
                  command: res4k
          - conditions:
              - condition: state
                entity_id: input_select.current_console
                state: "SNES"
            sequence:
              - service: remote.send_command
                target:
                  entity_id: remote.retrotink_4k_pro
                data:
                  command: res1080p

  # Power on sequence
  - alias: "RetroTINK: Gaming Setup Power On"
    trigger:
      platform: state
      entity_id: input_boolean.gaming_mode
      to: "on"
    action:
      - service: remote.turn_on
        target:
          entity_id: 
            - remote.retrotink_4k_pro
            - remote.retrotink_4k_ce
      - delay:
          seconds: 2
      - service: remote.send_command
        target:
          entity_id: remote.retrotink_4k_pro
        data:
          command: prof1

## Example script.yaml entries

script:
  # Quick profile cycling
  retrotink_next_profile:
    alias: "RetroTINK: Cycle to Next Profile"
    sequence:
      - service: remote.send_command
        target:
          entity_id: remote.retrotink_4k_pro
        data:
          command: prof
      - delay:
          milliseconds: 500
      - service: remote.send_command
        target:
          entity_id: remote.retrotink_4k_pro
        data:
          command: down
      - delay:
          milliseconds: 500
      - service: remote.send_command
        target:
          entity_id: remote.retrotink_4k_pro
        data:
          command: ok

  # Load specific profile directly
  retrotink_load_profile_3:
    alias: "RetroTINK: Load Profile 3"
    sequence:
      - service: remote.send_command
        target:
          entity_id: remote.retrotink_4k_pro
        data:
          command: prof3

  # Auto crop for 16:9 content
  retrotink_auto_crop_16_9:
    alias: "RetroTINK: Auto Crop 16:9"
    sequence:
      - service: remote.send_command
        target:
          entity_id: remote.retrotink_4k_pro
        data:
          command: aux3

  # Switch to 4K output
  retrotink_set_4k_output:
    alias: "RetroTINK: Set 4K Output"
    sequence:
      - service: remote.send_command
        target:
          entity_id: remote.retrotink_4k_pro
        data:
          command: res4k

  # Run auto phase calibration
  retrotink_auto_phase:
    alias: "RetroTINK: Auto Phase Calibration"
    sequence:
      - service: remote.send_command
        target:
          entity_id: remote.retrotink_4k_pro
        data:
          command: phase

  # Safe mode toggle
  retrotink_safe_mode:
    alias: "RetroTINK: Toggle Safe Mode"
    sequence:
      - service: remote.send_command
        target:
          entity_id: remote.retrotink_4k_pro
        data:
          command: safe

  # Complete power cycle
  retrotink_power_cycle:
    alias: "RetroTINK: Power Cycle"
    sequence:
      - service: remote.turn_off
        target:
          entity_id: remote.retrotink_4k_pro
      - delay:
          seconds: 3
      - service: remote.turn_on
        target:
          entity_id: remote.retrotink_4k_pro
      - delay:
          seconds: 2
      - service: remote.send_command
        target:
          entity_id: remote.retrotink_4k_pro
        data:
          command: prof1

## Example Lovelace Card Configuration

# Simple button card for common functions
type: button
name: Load Profile 1
icon: mdi:numeric-1-circle
tap_action:
  action: call-service
  service: remote.send_command
  target:
    entity_id: remote.retrotink_4k_pro
  data:
    command: prof1

# Grid of common commands
type: grid
cards:
  - type: button
    name: Menu
    icon: mdi:menu
    tap_action:
      action: call-service
      service: remote.send_command
      target:
        entity_id: remote.retrotink_4k_pro
      data:
        command: menu
  - type: button
    name: Profiles
    icon: mdi:tune
    tap_action:
      action: call-service
      service: remote.send_command
      target:
        entity_id: remote.retrotink_4k_pro
      data:
        command: prof
  - type: button
    name: Output
    icon: mdi:video
    tap_action:
      action: call-service
      service: remote.send_command
      target:
        entity_id: remote.retrotink_4k_pro
      data:
        command: output
  - type: button
    name: Input
    icon: mdi:import
    tap_action:
      action: call-service
      service: remote.send_command
      target:
        entity_id: remote.retrotink_4k_pro
      data:
        command: input
  - type: button
    name: Auto Phase
    icon: mdi:auto-fix
    tap_action:
      action: call-service
      service: remote.send_command
      target:
        entity_id: remote.retrotink_4k_pro
      data:
        command: phase
  - type: button
    name: Safe Mode
    icon: mdi:shield-check
    tap_action:
      action: call-service
      service: remote.send_command
      target:
        entity_id: remote.retrotink_4k_pro
      data:
        command: safe
columns: 2

# Resolution quick switch
type: horizontal-stack
cards:
  - type: button
    name: 4K
    icon: mdi:video-4k-box
    tap_action:
      action: call-service
      service: remote.send_command
      target:
        entity_id: remote.retrotink_4k_pro
      data:
        command: res4k
  - type: button
    name: 1440p
    icon: mdi:video-box
    tap_action:
      action: call-service
      service: remote.send_command
      target:
        entity_id: remote.retrotink_4k_pro
      data:
        command: res1440p
  - type: button
    name: 1080p
    icon: mdi:video-box
    tap_action:
      action: call-service
      service: remote.send_command
      target:
        entity_id: remote.retrotink_4k_pro
      data:
        command: res1080p

# Profile selector
type: grid
title: Quick Profile Access
cards:
  - type: button
    name: Profile 1
    tap_action:
      action: call-service
      service: remote.send_command
      target:
        entity_id: remote.retrotink_4k_pro
      data:
        command: prof1
  - type: button
    name: Profile 2
    tap_action:
      action: call-service
      service: remote.send_command
      target:
        entity_id: remote.retrotink_4k_pro
      data:
        command: prof2
  - type: button
    name: Profile 3
    tap_action:
      action: call-service
      service: remote.send_command
      target:
        entity_id: remote.retrotink_4k_pro
      data:
        command: prof3
  - type: button
    name: Profile 4
    tap_action:
      action: call-service
      service: remote.send_command
      target:
        entity_id: remote.retrotink_4k_pro
      data:
        command: prof4
columns: 4

# Navigation pad
type: vertical-stack
cards:
  - type: horizontal-stack
    cards:
      - type: button
        name: ""
        icon: mdi:blank
        tap_action:
          action: none
      - type: button
        name: Up
        icon: mdi:arrow-up
        tap_action:
          action: call-service
          service: remote.send_command
          target:
            entity_id: remote.retrotink_4k_pro
          data:
            command: up
      - type: button
        name: ""
        icon: mdi:blank
        tap_action:
          action: none
  - type: horizontal-stack
    cards:
      - type: button
        name: Left
        icon: mdi:arrow-left
        tap_action:
          action: call-service
          service: remote.send_command
          target:
            entity_id: remote.retrotink_4k_pro
          data:
            command: left
      - type: button
        name: OK
        icon: mdi:check-circle
        tap_action:
          action: call-service
          service: remote.send_command
          target:
            entity_id: remote.retrotink_4k_pro
          data:
            command: enter
      - type: button
        name: Right
        icon: mdi:arrow-right
        tap_action:
          action: call-service
          service: remote.send_command
          target:
            entity_id: remote.retrotink_4k_pro
          data:
            command: right
  - type: horizontal-stack
    cards:
      - type: button
        name: ""
        icon: mdi:blank
        tap_action:
          action: none
      - type: button
        name: Down
        icon: mdi:arrow-down
        tap_action:
          action: call-service
          service: remote.send_command
          target:
            entity_id: remote.retrotink_4k_pro
          data:
            command: down
      - type: button
        name: Back
        icon: mdi:arrow-left-circle
        tap_action:
          action: call-service
          service: remote.send_command
          target:
            entity_id: remote.retrotink_4k_pro
          data:
            command: back
