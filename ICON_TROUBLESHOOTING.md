# Icon Not Showing? Troubleshooting Guide

If the RetroTINK logo isn't displaying in Home Assistant, try these steps:

## 1. Hard Refresh Browser Cache

The most common issue is browser caching.

**Method 1: Hard Refresh**
- **Chrome/Edge**: Press `Ctrl + Shift + R` (Windows/Linux) or `Cmd + Shift + R` (Mac)
- **Firefox**: Press `Ctrl + F5` (Windows/Linux) or `Cmd + Shift + R` (Mac)
- **Safari**: Press `Cmd + Option + R`

**Method 2: Clear Home Assistant Frontend Cache**
1. Open Home Assistant
2. Go to **Developer Tools** → **Services**
3. Call service: `homeassistant.reload_config_entry`
4. Then call: `frontend.reload_themes`
5. Hard refresh your browser (Ctrl+Shift+R)

**Method 3: Clear Browser Cache Completely**
1. Open browser settings
2. Clear browsing data / cache
3. Restart browser
4. Log back into Home Assistant

## 2. Verify Files Are Installed

SSH into your Home Assistant and check:

```bash
ls -la /config/custom_components/retrotink/*.png
```

You should see:
- `icon.png` (27K)
- `icon@2x.png` (71K)  
- `logo.png` (27K)

If files are missing, reinstall the integration.

## 3. Restart Home Assistant

Sometimes a full restart is needed:

1. Go to **Settings** → **System**
2. Click **Restart**
3. Wait for restart to complete
4. Hard refresh browser

## 4. Check File Permissions

```bash
chmod 644 /config/custom_components/retrotink/*.png
```

## 5. Mobile App

If using the Home Assistant mobile app:
1. Close app completely
2. Clear app cache (in phone settings)
3. Reopen app

## 6. Check Home Assistant Version

The integration requires Home Assistant 2024.1.0 or newer. Check your version in **Settings** → **About**.

## 7. Still Not Working?

If the icon still doesn't appear after trying all the above:

1. The integration will still work perfectly - the icon is cosmetic only
2. Some Home Assistant installations have strict caching policies
3. Try a different browser
4. Check browser console for errors (F12 → Console tab)

## What the Icon Looks Like

The RetroTINK logo is white text on a black background with a distinctive satellite dish icon.

## Alternative: Use Card Icons

You can still use the RetroTINK logo in your Lovelace cards:

```yaml
type: button
entity: remote.retrotink_4k_pro
icon: mdi:video-vintage
name: RetroTINK Pro
```

Or download the logo and use it as a custom icon in your `/local/` folder.
