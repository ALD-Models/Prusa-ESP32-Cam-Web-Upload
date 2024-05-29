import requests
import json
import os

# Function to fetch the latest release info
def fetch_latest_release_info(repo_url):
    response = requests.get(repo_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch release info: {response.status_code}")

# Function to extract file URLs from the release info
def extract_file_urls(release_info):
    assets = release_info['assets']
    file_urls = {
        "bootloader": "",
        "partitions": "",
        "firmware": ""
    }

    for asset in assets:
        if 'bootloader.bin' in asset['name']:
            file_urls["bootloader"] = asset['browser_download_url']
        elif 'partitions.bin' in asset['name']:
            file_urls["partitions"] = asset['browser_download_url']
        elif 'ino.bin' in asset['name']:
            file_urls["firmware"] = asset['browser_download_url']
    
    return file_urls

# Function to update the manifest
def update_manifest(file_urls, manifest_path):
    manifest = {
        "name": "Prusa Cam",
        "version": "1.0.3-rc1",
        "new_install_prompt_erase": True,
        "builds": [
            {
                "chipFamily": "ESP32",
                "improv": True,
                "parts": [
                    { "path": file_urls["bootloader"], "offset": 4096 },
                    { "path": file_urls["partitions"], "offset": 32768 },
                    { "path": file_urls["firmware"], "offset": 65536 }
                ]
            }
        ]
    }
    
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=4)

# Main function
def main():
    repo_url = 'https://api.github.com/repos/prusa3d/Prusa-Firmware-ESP32-Cam/releases/latest'
    manifest_path = 'manifest.json'  # Update this path as needed

    try:
        # Fetch the latest release info
        release_info = fetch_latest_release_info(repo_url)
        
        # Extract file URLs
        file_urls = extract_file_urls(release_info)
        
        # Update the manifest
        update_manifest(file_urls, manifest_path)
        
        print("Manifest updated successfully.")
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
