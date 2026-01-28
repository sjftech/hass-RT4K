# Adding the RetroTINK Logo to Home Assistant

Custom integration icons don't live in the integration itself - they're hosted on Home Assistant's centralized brands repository at `https://brands.home-assistant.io/`.

## How to Submit the Logo

To get the RetroTINK logo to appear in Home Assistant, you need to submit it to the Home Assistant Brands repository:

### Step 1: Prepare the Icon Files

You need to create properly formatted icon files:

1. **icon.png** - 512x512 pixels, square, PNG format
2. **icon@2x.png** (optional) - 1024x1024 pixels for high-DPI displays
3. **logo.png** (optional) - Can be rectangular if you want a different logo vs icon

Requirements:
- PNG format only
- Square aspect ratio for icon
- Properly trimmed (no extra whitespace)
- Optimized and compressed
- Transparent or white background preferred

### Step 2: Fork the Brands Repository

1. Go to https://github.com/home-assistant/brands
2. Click "Fork" in the top right to create your own copy

### Step 3: Add Your Icons

1. In your fork, navigate to `custom_integrations/`
2. Create a new folder named `retrotink` (must match your domain in manifest.json)
3. Upload your `icon.png` (and optionally `icon@2x.png` and `logo.png`)

### Step 4: Create a Pull Request

1. Commit your changes with a message like: "Add RetroTINK-4K integration icons"
2. Create a Pull Request from your fork to the main brands repository
3. Wait for Home Assistant team to review and merge

### Step 5: Wait for Deployment

Once merged:
- Icons are cached for 24 hours on Cloudflare
- Browsers cache for 7 days
- You may need to wait and clear your browser cache

## Alternative: Use the Icon Files Provided

I've prepared the proper icon files for you. They're in this repository:

- Properly sized (512x512)
- Correct PNG format
- Square aspect ratio
- Black background (as RetroTINK logo is white on black)

## Current Status

**The integration will work perfectly without the icon** - it will just show a placeholder. The icon is purely cosmetic. Once you submit to the brands repo and it's approved, the icon will appear for all users automatically.

## Example: How Other Integrations Do It

Check out examples in the brands repo:
- https://github.com/home-assistant/brands/tree/master/custom_integrations/unfoldedcircle
- https://github.com/home-assistant/brands/tree/master/custom_integrations

## Icon Files Location

The prepared icon files are in a separate `icon_files/` directory in this repository, ready for you to submit to the brands repo.
