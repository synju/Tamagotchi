import logging
from flask import Flask, jsonify, request

app = Flask(__name__)

# Suppress Flask (werkzeug) logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Initialize Tamagotchi instance globally
tamagotchi_instance = None  # This will hold the reference to the Tamagotchi instance


class TamagotchiAPI:
	def __init__(self, tamagotchi):
		global tamagotchi_instance
		tamagotchi_instance = tamagotchi  # Assign the Tamagotchi instance to global

	def start_api(self):
		app.run(host='0.0.0.0', port=5000)


@app.route('/status', methods=['GET'])
def get_status():
	global tamagotchi_instance
	if tamagotchi_instance:
		status = {
			'name': tamagotchi_instance.name,
			'health': tamagotchi_instance.health,
			'hunger': tamagotchi_instance.hunger,
			'happiness': tamagotchi_instance.happiness,
			'hygiene': tamagotchi_instance.hygiene,
			'age': tamagotchi_instance.age,
			'sleeping': tamagotchi_instance.sleeping,
			'pc_vars': {
				'volume': tamagotchi_instance.pc_volume,
			}
		}
		return jsonify(status)
	else:
		return jsonify({"error": "Tamagotchi instance not found"}), 500


@app.route('/action', methods=['POST'])
def perform_action():
	global tamagotchi_instance
	data = request.json
	action = data.get('action', None)

	if tamagotchi_instance and action:
		if action == 'feed':
			tamagotchi_instance.feed(silent=True)
		elif action == 'clean':
			tamagotchi_instance.clean(silent=True)
		elif action == 'play':
			tamagotchi_instance.play(silent=True)
		elif action == 'medicine':
			tamagotchi_instance.give_medicine(silent=True)
		return jsonify({'message': f'Action {action} performed'})
	return jsonify({'message': 'Invalid action'}), 400


# New route to set PC volume
@app.route('/set_volume', methods=['POST'])
def set_volume():
	global tamagotchi_instance
	data = request.json
	new_volume = data.get('volume', None)

	if tamagotchi_instance and new_volume is not None:
		# Ensure volume is between 0 and 100
		if 0 <= new_volume <= 100:
			tamagotchi_instance.pc_volume = new_volume
			return jsonify({'message': f'Volume set to {new_volume}'})
		else:
			return jsonify({'message': 'Volume must be between 0 and 100'}), 400
	return jsonify({'message': 'Invalid volume or Tamagotchi instance not found'}), 400


@app.route('/shutdown', methods=['POST'])
def shutdown():
	"""Gracefully shut down the API server."""
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()
	return 'Server shutting down...'
