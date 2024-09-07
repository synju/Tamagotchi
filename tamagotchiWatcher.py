import requests
import os
import time

# The URL of your Tamagotchi API
API_URL = "http://129.232.182.162:5000/status"

# Variable to store the last known volume
last_known_volume = None


# Function to fetch status from the API
def get_tamagotchi_status():
	try:
		response = requests.get(API_URL)
		if response.status_code == 200:
			return response.json()
		else:
			print(f"Error: Failed to retrieve status. Status code: {response.status_code}")
			return None
	except Exception as e:
		print(f"Error: {str(e)}")
		return None


# Function to check and adjust PC volume
def adjust_pc_volume():
	global last_known_volume  # Use the global variable to track last known volume
	status = get_tamagotchi_status()
	if status:
		volume = status.get('pc_vars', {}).get('volume', 1)  # Default volume to 1 if not found

		# Check if the volume has changed
		if last_known_volume != volume:
			if volume == 0:
				print("Setting PC volume to 0")
				os.system("nircmd.exe mutesysvolume 1")  # Mute the system volume
			else:
				print(f"Setting PC volume to {volume}")
				os.system(f"nircmd.exe setsysvolume {volume * 65535 // 100}")  # Adjust the volume

			# Update the last known volume
			last_known_volume = volume
		else:
			print(f"Volume already set to {volume}. No changes needed.")


if __name__ == "__main__":
	# Continuous loop to run the function every 5 seconds
	while True:
		print("Awaiting instructions...")
		adjust_pc_volume()
		time.sleep(5)  # Wait for 5 seconds before running the function again
