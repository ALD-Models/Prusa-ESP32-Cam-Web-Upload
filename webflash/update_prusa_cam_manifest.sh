#!/bin/bash

# GitHub repository information
REPO_OWNER="prusa3d"
REPO_NAME="Prusa-Firmware-ESP32-Cam"

# GitHub API URL for the latest release
LATEST_RELEASE_URL="https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/releases/latest"

# Fetch the latest release information
LATEST_RELEASE=$(curl -s $LATEST_RELEASE_URL)

# Extract the asset URLs
BOOTLOADER_URL=$(echo $LATEST_RELEASE | jq -r '.assets[] | select(.name | contains("bootloader.bin")) | .browser_download_url')
PARTITIONS_URL=$(echo $LATEST_RELEASE | jq -r '.assets[] | select(.name | contains("partitions.bin")) | .browser_download_url')
FIRMWARE_URL=$(echo $LATEST_RELEASE | jq -r '.assets[] | select(.name | contains("ino.bin")) | .browser_download_url')
VERSION_TAG=$(echo $LATEST_RELEASE | jq -r '.tag_name')

# Check if all necessary files were found
if [ -z "$BOOTLOADER_URL" ] || [ -z "$PARTITIONS_URL" ] || [ -z "$FIRMWARE_URL" ]; then
    echo "Error: Not all required bin files were found in the latest release."
    exit 1
fi

# Create the manifest with the latest URLs
MANIFEST=$(cat <<EOF
{
    "name": "Prusa Cam",
    "version": "$VERSION_TAG",
    "new_install_prompt_erase": true,
    "builds": [
        {
            "chipFamily": "ESP32",
            "improv": true,
            "parts": [
                { "path": "$BOOTLOADER_URL", "offset": 4096 },
                { "path": "$PARTITIONS_URL", "offset": 32768 },
                { "path": "$FIRMWARE_URL", "offset": 65536 }
            ]
        }
    ]
}
EOF
)

# Output the manifest to a file
echo "$MANIFEST" > manifest.json
echo "Manifest file created successfully."
