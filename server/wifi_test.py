import subprocess

ssid = 'Mac-Events'

# Command to switch Wi-Fi network
command = f'networksetup -setairportnetwork en0 "{ssid}"'

# Execute the command
subprocess.run(command, shell=True)