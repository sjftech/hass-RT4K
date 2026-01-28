# Publishing to GitHub - Step-by-Step Guide

This guide will help you publish the RetroTINK-4K Serial Remote Control integration to GitHub.

## Prerequisites

- A GitHub account
- Git installed on your computer
- The integration files (retrotink_integration_v1.0.0_FINAL.zip)

## Step 1: Create a New Repository on GitHub

1. Go to https://github.com
2. Click the "+" button in the top right → "New repository"
3. Fill in the details:
   - **Repository name**: `hass-retrotink` (or `retrotink-homeassistant`)
   - **Description**: "Home Assistant integration for RetroTINK-4K Pro and CE serial control"
   - **Public** (check this box)
   - **Do NOT** initialize with README (we already have one)
   - **Do NOT** add .gitignore
   - **Do NOT** choose a license (we have MIT in the files)
4. Click "Create repository"

## Step 2: Prepare Your Local Files

1. Extract `retrotink_integration_v1.0.0_FINAL.zip`
2. Rename the extracted folder from `retrotink_integration` to your repository name (e.g., `hass-retrotink`)
3. Open a terminal/command prompt in that directory

## Step 3: Initialize Git and Push to GitHub

Run these commands in order (replace `yourusername` with your actual GitHub username):

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial release v1.0.0"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/hass-retrotink.git

# Push to GitHub
git push -u origin main
```

If you get an error about "main" vs "master", try:
```bash
git branch -M main
git push -u origin main
```

## Step 4: Create a Release

1. Go to your repository on GitHub
2. Click on "Releases" (right sidebar)
3. Click "Create a new release"
4. Fill in the release details:
   - **Tag version**: `v1.0.0`
   - **Release title**: `v1.0.0 - Initial Release`
   - **Description**: Copy from CHANGELOG.md
5. Attach the zip file (optional but recommended)
6. Click "Publish release"

## Step 5: Update Repository Settings

### Add Topics
1. Go to your repository main page
2. Click the gear icon next to "About"
3. Add topics: `home-assistant`, `homeassistant`, `retrotink`, `hacs`, `custom-component`, `integration`
4. Add website: `https://www.retrotink.com`
5. Click "Save changes"

### Create a Nice README Badge
The README already has a placeholder. Update this line in README.md:
```markdown
[![GitHub release](https://img.shields.io/github/release/yourusername/hass-retrotink.svg)](https://GitHub.com/yourusername/hass-retrotink/releases/)
```
Replace `yourusername` with your actual username.

## Step 6: Test the Installation

Test that users can install it:

1. Go to Home Assistant
2. Go to HACS → Integrations
3. Click three dots (top right) → Custom repositories
4. Add your repository URL: `https://github.com/yourusername/hass-retrotink`
5. Category: Integration
6. It should appear and be installable

## Step 7: Submit to HACS Default (Optional)

To get your integration into the default HACS store:

1. Make sure your repository has been public for at least 2 weeks
2. Fork https://github.com/hacs/default
3. Edit `integration` file
4. Add your repository in alphabetical order
5. Create a Pull Request

Requirements:
- Repository must be public
- Must have releases with tags
- Must have proper README
- Must follow HACS requirements

## Step 8: Submit Icon to Home Assistant Brands (Optional)

To get the RetroTINK logo showing:

1. Fork https://github.com/home-assistant/brands
2. Create folder: `custom_integrations/retrotink/`
3. Upload the icon files from `icon_files_for_brands_repo/`
4. Create a Pull Request

See `ADDING_LOGO.md` for detailed instructions.

## Future Updates

When you want to release updates:

```bash
# Make your changes to the code
git add .
git commit -m "Description of changes"
git push

# Create a new release on GitHub with new version number
# Don't forget to update the version in manifest.json first!
```

## Getting Help

If you run into issues:
- Check GitHub's documentation: https://docs.github.com
- HACS documentation: https://hacs.xyz/docs/publish/integration
- Home Assistant developer docs: https://developers.home-assistant.io

## Repository Structure

Your final repository should look like:
```
hass-retrotink/
├── .github/
│   └── ISSUE_TEMPLATE.md
├── custom_components/
│   └── retrotink/
│       ├── translations/
│       ├── __init__.py
│       ├── config_flow.py
│       ├── const.py
│       ├── manifest.json
│       ├── remote.py
│       ├── services.yaml
│       └── strings.json
├── icon_files_for_brands_repo/
├── ADDING_LOGO.md
├── CHANGELOG.md
├── COMMAND_REFERENCE.md
├── EXAMPLES.md
├── hacs.json
├── LICENSE
├── README.md
├── QUICKSTART.md
└── UNFOLDED_CIRCLE.md
```

## Quick Command Reference

```bash
# Clone your repo (for future edits)
git clone https://github.com/yourusername/hass-retrotink.git
cd hass-retrotink

# Make changes, then:
git add .
git commit -m "Your commit message"
git push

# Create new release on GitHub website with new version tag
```

Good luck with your publication! 🚀
