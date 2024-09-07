import random
import sys
import time
import os
import json
import datetime
import platform
import tweepy
import threading
from peach_api import TamagotchiAPI


class Tamagotchi:
	STATE_MENU = 0
	STATE_STATS = 1
	STATE_FEED = 2
	STATE_PLAY = 3
	STATE_CLEAN = 4
	STATE_MEDICINE = 5
	STATE_EXIT = 6
	STATE_DEATH = 7
	STATE_SLEEPING = 8

	DECAY_INTERVAL = 60 * 60  # 60 Minutes

	# DECAY_INTERVAL = 5 * 60  # 5 Minutes
	# DECAY_INTERVAL = 1 * 60  # 1 Minute
	# DECAY_INTERVAL = 1 * 10  # 10 Seconds

	def __init__(self):
		self.state = self.STATE_MENU
		self.action = 1
		self.name = ""
		self.health = 4
		self.hunger = 4
		self.happiness = 4
		self.hygiene = 4
		self.age = 0
		self.save_time = self.get_current_time_ms()
		self.last_decay_time = self.get_current_time_ms()
		self.creation_date_and_time = self.get_current_time_ms()
		self.sleeping = self.is_sleeping()
		self.last_updated = self.get_current_time_ms()
		self.api = TamagotchiAPI(self)  # Pass the current Tamagotchi instance to API
		threading.Thread(target=self.api.start_api, daemon=True).start()  # Start API in another thread

	def post_tweet(self, tweet):
		# Bearer token
		bearer_token = "AAAAAAAAAAAAAAAAAAAAAAvQowEAAAAANEgvbSUz9ePm4wm1GQlCqs%2BO%2B3c%3Dkb8xTZIK5zxFfDl7ywVk0MWSwIwe4bD2B0dPhp09JRVqx9Ohzu"

		# Define keys
		consumer_key = "TSxot5ao01PooO73teabMlNr2"
		consumer_secret = "v9dz6mP5bMZrJVyylGtugcKoVfozvYgy8ZrDEO1lJRO40KDzLe"

		# Access
		access_token = "1682725687260487681-c9ak4H2Bb0z3QovxH9LEMS1dssf0eJ"
		access_token_secret = "adYOGyStHrybIQhRMSrlSLfKYHKbLfSx8vI688lta1bqn"

		client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

		# Post the tweet
		try:
			response = client.create_tweet(text=tweet)
		except Exception as e:
			print(str(e))  # sys.exit()

	def load_tweets(self, filename):
		# Load tweets from a JSON file and return them as a list.
		try:
			with open(filename, 'r') as file:
				tweets = json.load(file)
			return tweets
		except FileNotFoundError:
			print(f"File '{filename}' not found.")
			return []
		except json.JSONDecodeError:
			print(f"Error decoding JSON in '{filename}'.")
			return []

	def save_tweets(self, tweets, filename):
		# Save tweets to "filename"
		with open(filename, 'w') as file:
			json.dump(tweets, file)

	def get_twitter_username(self):
		# Bearer token
		bearer_token = "AAAAAAAAAAAAAAAAAAAAAAvQowEAAAAANEgvbSUz9ePm4wm1GQlCqs%2BO%2B3c%3Dkb8xTZIK5zxFfDl7ywVk0MWSwIwe4bD2B0dPhp09JRVqx9Ohzu"

		# Define keys
		consumer_key = "TSxot5ao01PooO73teabMlNr2"
		consumer_secret = "v9dz6mP5bMZrJVyylGtugcKoVfozvYgy8ZrDEO1lJRO40KDzLe"

		# Access
		access_token = "1682725687260487681-c9ak4H2Bb0z3QovxH9LEMS1dssf0eJ"
		access_token_secret = "adYOGyStHrybIQhRMSrlSLfKYHKbLfSx8vI688lta1bqn"

		client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

		try:
			# Fetch the authenticated user
			user_info = client.get_me()
			print(f"Twitter Bot Username: @{user_info.data.username}")
		except Exception as e:
			print(f"Failed to get Twitter username: {str(e)}")

		time.sleep(5)

	def is_sleeping(self):
		current_time = datetime.datetime.now().time()
		return current_time >= datetime.time(21) or current_time < datetime.time(9)

	def is_valid_integer(self, value):
		return isinstance(value, int)

	def clear_terminal(self):
		if platform.system() == 'Windows':
			os.system('cls')  # For Windows
		else:
			os.system('clear')  # For Linux/Unix and macOS

	def get_current_time_ms(self):
		return int(time.time() * 1000)

	def reset_creation_time(self):
		self.creation_date_and_time = self.get_current_time_ms()

	def start(self):
		self.load_stats()
		if len(self.name) == 0:
			self.set_name(input("Enter a name for your Tamagotchi: "))

		# Print the Twitter bot's username
		# self.get_twitter_username()

		# Start the background thread to refresh the display every minute
		refresh_thread = threading.Thread(target=self.refresh_display_periodically)
		refresh_thread.daemon = True  # Ensure the thread exits when the main program exits
		refresh_thread.start()

		self.process_input()

	def save_stats(self):
		# Get the current directory
		current_dir = os.path.dirname(os.path.abspath(__file__))

		# Create the file path for saving
		save_path = os.path.join(current_dir, 'tamagotchi_stats.json')

		# Create the data dictionary
		data = {'name': self.name,  # Add this line to save the name
						'health': self.health, 'hunger': self.hunger, 'happiness': self.happiness, 'hygiene': self.hygiene, 'age': self.age, 'saveTime': self.save_time, 'lastDecayTime': self.last_decay_time, 'creationDateTime': self.creation_date_and_time, 'sleeping': self.sleeping, 'lastUpdated': self.last_updated, }

		# Save the data to the file
		with open(save_path, 'w') as file:
			json.dump(data, file)

	def load_stats(self):
		# Get the current directory
		current_dir = os.path.dirname(os.path.abspath(__file__))

		# Create the file path for loading
		load_path = os.path.join(current_dir, 'tamagotchi_stats.json')

		# Check if the file exists
		if not os.path.exists(load_path):
			print("No saved stats found.")
			return

		# Load the data from the file
		with open(load_path, 'r') as file:
			data = json.load(file)

		# Update the Tamagotchi's stats
		self.name = data.get('name', self.name)  # Add this line to load the name
		self.health = data.get('health', self.health)
		self.hunger = data.get('hunger', self.hunger)
		self.happiness = data.get('happiness', self.happiness)
		self.hygiene = data.get('hygiene', self.hygiene)
		self.age = data.get('age', self.age)
		self.save_time = data.get('saveTime', self.save_time)
		self.last_decay_time = data.get('lastDecayTime', self.last_decay_time)
		self.creation_date_and_time = data.get('creationDateTime', self.creation_date_and_time)
		self.sleeping = data.get('sleeping', self.sleeping)
		self.last_updated = data.get('lastUpdated', self.last_updated)  # Add this line to load last_updated

		# Update sleeping state during daytime
		if not self.is_sleeping():
			self.sleeping = False

		# Update last_decay_time based on elapsed time since last decay
		current_time = self.get_current_time_ms()
		time_difference = current_time - self.last_decay_time

		# If the last decay time was before 9am on the current day,
		# update the last_decay_time to 9am on the current day.
		last_decay_datetime = datetime.datetime.fromtimestamp(self.last_decay_time / 1000)
		current_datetime = datetime.datetime.now()
		if last_decay_datetime.date() < current_datetime.date():
			nine_am_today = current_datetime.replace(hour=9, minute=0, second=0, microsecond=0)
			self.last_decay_time = int(nine_am_today.timestamp() * 1000)

		# Update last_decay_time to the correct value
		self.last_decay_time = current_time - (time_difference % (self.DECAY_INTERVAL * 1000))

	def set_name(self, name):
		self.name = name

	def refresh_display_periodically(self):
		time.sleep(60)  # Wait for 60 seconds before first refresh

		# This function runs in a separate thread and refreshes the display every minute.
		while True:
			self.process_input()  # Call process_input to refresh the display
			time.sleep(60)  # Wait for 60 seconds before refreshing again

	def decay(self):
		current_time = self.get_current_time_ms()

		# Calculate the time difference in milliseconds between the current time and the last decay time
		time_difference = current_time - self.last_decay_time

		# Calculate the intervals passed since the last decay based on the DECAY_INTERVAL
		intervals_passed = time_difference // (self.DECAY_INTERVAL * 1000)

		# Update last_decay_time to the correct value
		self.last_decay_time += intervals_passed * (self.DECAY_INTERVAL * 1000)

		if self.sleeping:
			self.last_decay_time = current_time - (time_difference % (self.DECAY_INTERVAL * 1000))
			return

		if self.health > 0:
			self.age += intervals_passed

		if intervals_passed > 0:
			self.hunger -= intervals_passed
			self.hunger = max(self.hunger, 0)  # Ensure hunger doesn't go below 0

			self.happiness -= intervals_passed
			self.happiness = max(self.happiness, 0)  # Ensure happiness doesn't go below 0

			if intervals_passed % 3 == 0:
				self.hygiene -= 1
				self.hygiene = max(self.hygiene, 0)  # Ensure hygiene doesn't go below 0

			if self.health > 0:
				if self.hunger <= 1 or self.hygiene <= 1:
					self.health -= intervals_passed
					self.health = max(self.health, 0)  # Ensure health doesn't go below 0
					self.happiness -= intervals_passed
					self.happiness = max(self.happiness, 0)  # Ensure happiness doesn't go below 0

			self.last_updated = current_time  # Update last_updated at the end of decay

		# Check for Tamagotchi's death
		if self.health == 0:
			self.state = self.STATE_DEATH
			self.print_health_bar()
			self.save_stats()
			return

		self.save_stats()  # Save the stats after decay

	def update_last_updated(self):
		# Update last_updated with the current time
		self.last_updated = self.get_current_time_ms()

	def print_health_bar(self):
		if self.health == 0:
			print("[----] Health")
		if self.health == 1:
			print("[♡---] Health")
		if self.health == 2:
			print("[♡♡--] Health")
		if self.health == 3:
			print("[♡♡♡-] Health")
		if self.health == 4:
			print("[♡♡♡♡] Health")

	def print_hunger_bar(self):
		if self.hunger == 0:
			print("[----] Hunger")
		if self.hunger == 1:
			print("[♡---] Hunger")
		if self.hunger == 2:
			print("[♡♡--] Hunger")
		if self.hunger == 3:
			print("[♡♡♡-] Hunger")
		if self.hunger == 4:
			print("[♡♡♡♡] Hunger")

	def print_happiness_bar(self):
		if self.happiness == 0:
			print("[----] Happiness")
		if self.happiness == 1:
			print("[♡---] Happiness")
		if self.happiness == 2:
			print("[♡♡--] Happiness")
		if self.happiness == 3:
			print("[♡♡♡-] Happiness")
		if self.happiness == 4:
			print("[♡♡♡♡] Happiness")

	def print_hygiene_bar(self):
		if self.hygiene == 0:
			print("[----] Hygiene")
		if self.hygiene == 1:
			print("[♡---] Hygiene")
		if self.hygiene == 2:
			print("[♡♡--] Hygiene")
		if self.hygiene == 3:
			print("[♡♡♡-] Hygiene")
		if self.hygiene == 4:
			print("[♡♡♡♡] Hygiene")

	def print_age(self):
		current_time = self.get_current_time_ms()
		elapsed_time = current_time - self.creation_date_and_time
		age_timedelta = datetime.timedelta(milliseconds=elapsed_time)

		years, remainder = divmod(age_timedelta.days, 365)
		months, days = divmod(remainder, 30)  # Simplified calculation, ignoring leap years and variations in month lengths.
		hours, remainder = divmod(age_timedelta.seconds, 3600)
		minutes, seconds = divmod(remainder, 60)

		age_parts = []

		if years > 0:
			age_parts.append(f"{years} year{'s' if years != 1 else ''}")
		if months > 0:
			age_parts.append(f"{months} month{'s' if months != 1 else ''}")
		if days > 0:
			age_parts.append(f"{days} day{'s' if days != 1 else ''}")
		if hours > 0:
			age_parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
		if minutes > 0:
			age_parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
		if seconds > 0:
			age_parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

		age_str = ", ".join(age_parts)
		print("Age:", age_str)

	def print_menu_state(self):
		print("1. Feed")
		print("2. Do Something Fun!!!")
		print("3. Clean")
		print("4. Medicine")
		print("5. Save & Exit")

	def print_decay_details(self):
		# Last Updated
		last_updated_datetime = datetime.datetime.fromtimestamp(self.last_updated / 1000)
		last_updated_str = last_updated_datetime.strftime("%A %d %B %#I:%M%p")
		print("Last Update:", last_updated_str)

		# Rate of Decay
		rate_of_decay_timedelta = datetime.timedelta(seconds=self.DECAY_INTERVAL)
		rate_of_decay_str = str(rate_of_decay_timedelta)

		days = rate_of_decay_timedelta.days
		hours, remainder = divmod(rate_of_decay_timedelta.seconds, 3600)
		minutes, seconds = divmod(remainder, 60)

		rate_of_decay_parts = []
		if days > 0:
			rate_of_decay_parts.append(f"{days} day{'s' if days != 1 else ''}")
		if hours > 0:
			rate_of_decay_parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
		if minutes > 0:
			rate_of_decay_parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
		if seconds > 0:
			rate_of_decay_parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

		rate_of_decay_str = ", ".join(rate_of_decay_parts)
		print("Update Frequency:", rate_of_decay_str)

		# Remaining Time
		remaining_time = self.last_decay_time + self.DECAY_INTERVAL * 1000 - self.get_current_time_ms()
		remaining_timedelta = datetime.timedelta(milliseconds=remaining_time)
		remaining_hours = remaining_timedelta.seconds // 3600
		remaining_minutes = (remaining_timedelta.seconds % 3600) // 60
		remaining_seconds = remaining_timedelta.seconds % 60

		if remaining_time > 0:
			current_datetime = datetime.datetime.now()
			nine_am_today = current_datetime.replace(hour=9, minute=0, second=0, microsecond=0)

			remaining_time_str = ""
			if current_datetime >= nine_am_today:
				# Next update is past 9 PM, display the regular remaining time
				if remaining_hours > 0:
					remaining_time_str += f"{remaining_hours} hour{'s' if remaining_hours != 1 else ''}, "
				if remaining_minutes > 0:
					remaining_time_str += f"{remaining_minutes} minute{'s' if remaining_minutes != 1 else ''}, "
				remaining_time_str += f"{remaining_seconds} second{'s' if remaining_seconds != 1 else ''}"
			else:
				# Next update is before 9 PM, display "Tomorrow 9am"
				tomorrow_nine_am = nine_am_today + datetime.timedelta(days=1)
				remaining_time_str = tomorrow_nine_am.strftime("Tomorrow %I:%M%p")

			print("Next Update:", remaining_time_str)

	def print_feed_state(self):
		self.print_hunger_bar()
		print("1. Give Food")
		print("2. Back")

	def print_play_state(self):
		self.print_happiness_bar()
		print("1. Tweet or play a game!!!")
		print("2. Back")

	def print_clean_state(self):
		self.print_hygiene_bar()
		print("1. Clean")
		print("2. Back")

	def print_medicine_state(self):
		self.print_health_bar()
		print("1. Give Medicine")
		print("2. Back")

	def print_death_state(self):
		print(f"Your Tamagotchi is dead. How could you let that happen, what is wrong with you?")
		print("1. Restart")
		print("2. Exit")

	def restart(self):
		print("Restarting...")
		time.sleep(1)
		self.health = 4
		self.hunger = 4
		self.happiness = 4
		self.hygiene = 4
		self.age = 0
		self.last_decay_time = self.get_current_time_ms()
		self.reset_creation_time()
		self.state = self.STATE_MENU
		self.save_stats()
		self.process_input()

	def exit(self):
		self.save_stats()
		print("Saving and exiting...")
		time.sleep(1)
		sys.exit()

	def print_name(self):
		if len(self.name) > 0:
			print(f"Name: {self.name}")

	def print_sleeping(self):
		print("zZz... zZz... Check back at 9am.")
		self.print_health_bar()
		self.print_happiness_bar()
		print("1. Exit")
		self.state = self.STATE_SLEEPING

	def display_state(self):
		# Clear Terminal
		self.clear_terminal()

		print("<--------------------------->")
		print("<------ Tamagotchi!!! ------>")
		print("<--------------------------->")

		# Print Stuff
		self.print_name()
		self.print_age()

		# Always stats and decay details.
		self.print_decay_details()
		self.print_health_bar()
		self.print_hunger_bar()
		self.print_hygiene_bar()
		self.print_happiness_bar()

		# Check if sleeping...
		if self.is_sleeping():
			self.state = self.STATE_SLEEPING

		# Other States...
		if self.state == self.STATE_MENU:
			self.print_menu_state()
		elif self.state == self.STATE_FEED:
			self.print_feed_state()
		elif self.state == self.STATE_PLAY:
			self.print_play_state()
		elif self.state == self.STATE_CLEAN:
			self.print_clean_state()
		elif self.state == self.STATE_MEDICINE:
			self.print_medicine_state()
		elif self.state == self.STATE_EXIT:
			self.exit()
		elif self.state == self.STATE_DEATH:
			self.print_death_state()
		elif self.state == self.STATE_SLEEPING:
			self.print_sleeping()

	# Action Methods
	def check_and_update_from_json(self):
		# Read the current stats from the JSON file and update the Tamagotchi instance
		try:
			with open('tamagotchi_stats.json', 'r') as file:
				data = json.load(file)
			self.health = data['health']
			self.hunger = data['hunger']
			self.happiness = data['happiness']
			self.hygiene = data['hygiene']
			self.age = data['age']
			self.name = data['name']
			self.sleeping = data['sleeping']
		except FileNotFoundError:
			print("Stats file not found.")
		except json.JSONDecodeError:
			print("Error reading the JSON file.")

	def feed(self, silent=False):
		self.check_and_update_from_json()
		if self.hunger < 4:
			if not silent:
				print("Feeding...")
			self.hunger += 1
		else:
			if not silent:
				print("Can't eat anymore...")
		time.sleep(1)
		self.update_last_updated()
		self.save_stats()

	def clean(self, silent=False):
		self.check_and_update_from_json()
		if not silent:
			print("Cleaning...")
		self.hygiene = 4
		time.sleep(1)
		self.update_last_updated()
		self.save_stats()

	def play(self, silent=False):
		self.check_and_update_from_json()

		default_tweet = "Having a great time with my Tamagotchi! #Tamagotchi #FunTimes"
		if self.happiness < 4:
			tweets = self.load_tweets("tweets.json")
			if not tweets:  # Check if the list is empty
				if not silent:
					print("Posted a tweet:", default_tweet)
			else:
				tweet = random.choice(tweets)
				# Start a new thread to post the tweet
				tweet_thread = threading.Thread(target=self.post_tweet, args=(tweet,))
				tweet_thread.start()
				if not silent:
					print("Posted a tweet:", tweet)
			self.happiness += 1
		else:
			if not silent:
				print("Posted a tweet:", default_tweet)
			if self.happiness < 4:
				self.happiness += 1

			time.sleep(5)

		self.update_last_updated()
		self.save_stats()

	def give_medicine(self, silent=False):
		self.check_and_update_from_json()
		if self.health < 4:
			if not silent:
				print("Giving medicine...")
			self.health = 4
		else:
			if not silent:
				print("At full health already...")
		time.sleep(1)
		self.update_last_updated()
		self.save_stats()

	# Process Input
	def process_input(self):
		if self.state != self.STATE_EXIT:
			self.decay()
		self.display_state()

		# Ensure the "Select an action:" prompt always remains
		if self.state == self.STATE_MENU:
			print("Select an action: ", end="")

		# Get Input
		user_input = input()
		if user_input.strip() != "":
			try:
				self.action = int(user_input)
			except ValueError:
				print("Unknown input, try again...")
				self.process_input()
		else:
			print("Unknown input, try again...")
			self.process_input()

		# Handle Input
		if self.is_valid_integer(self.action):
			# MENU
			if self.state == self.STATE_MENU:
				if self.action == 1:  # 1. Feed
					self.state = self.STATE_FEED
				if self.action == 2:  # 2. Play
					self.state = self.STATE_PLAY
				if self.action == 3:  # 3. Clean
					self.state = self.STATE_CLEAN
				if self.action == 4:  # 4. Medicine
					self.state = self.STATE_MEDICINE
				if self.action == 5:  # 5. Save & Exit
					self.state = self.STATE_EXIT
				self.save_stats()
				self.process_input()

			# FEED
			if self.state == self.STATE_FEED:
				if self.action == 1:  # 1. Feed
					self.feed()
				if self.action == 2:  # 2. Back
					self.state = self.STATE_MENU
				self.process_input()

			# PLAY
			if self.state == self.STATE_PLAY:
				if self.action == 1:  # 1. Do something fun...
					self.play()
				if self.action == 2:  # 2. Back
					self.state = self.STATE_MENU
				self.process_input()

			# CLEAN
			if self.state == self.STATE_CLEAN:
				if self.action == 1:  # 1. Clean
					self.clean()
				if self.action == 2:  # 2. Back
					self.state = self.STATE_MENU
				self.process_input()

			# MEDICINE
			if self.state == self.STATE_MEDICINE:
				if self.action == 1:  # 1. Give Medicine
					self.give_medicine()
				if self.action == 2:  # 2. Back
					self.state = self.STATE_MENU
				self.process_input()

			# DEATH
			if self.state == self.STATE_DEATH:
				if self.action == 1:  # 1. Restart
					self.restart()
				if self.action == 2:  # 2. Exit
					self.state = self.STATE_EXIT
				self.process_input()

			# SLEEPING
			if self.state == self.STATE_SLEEPING:
				if self.action == 1:  # 1. Exit
					self.exit()


# Start Tamagotchi
Tamagotchi().start()
