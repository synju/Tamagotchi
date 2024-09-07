# peach_api.py

from flask import Flask, jsonify, request

app = Flask(__name__)


class TamagotchiAPI:
	def __init__(self, tamagotchi_instance):
		self.tamagotchi = tamagotchi_instance

	def start_api(self):
		# Start the Flask server (could be threaded later)
		app.run(host='0.0.0.0', port=5000)


@app.route('/status', methods=['GET'])
def get_status():
	# Return Peach's current stats
	status = {'name': self.tamagotchi.name, 'health': self.tamagotchi.health, 'hunger': self.tamagotchi.hunger, 'happiness': self.tamagotchi.happiness, 'hygiene': self.tamagotchi.hygiene, 'age': self.tamagotchi.age, 'sleeping': self.tamagotchi.sleeping}
	return jsonify(status)


@app.route('/action', methods=['POST'])
def perform_action():
	data = request.json
	action = data.get('action', None)
	if action:
		if action == 'feed':
			self.tamagotchi.feed()
		elif action == 'clean':
			self.tamagotchi.clean()
		elif action == 'play':
			self.tamagotchi.play()
		elif action == 'medicine':  # Added medicine action
			self.tamagotchi.give_medicine()
		return jsonify({'message': f'Action {action} performed'})
	return jsonify({'message': 'Invalid action'}), 400
