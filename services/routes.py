import json
from data.models import Plant, HumidityLog
from flask import Flask, request, jsonify


app = Flask(__name__)

# Helper function to convert model objects to dicts for JSON serialization
def plant_to_dict(plant):
    return {"id": plant.id, "name": plant.name}

def humidity_log_to_dict(log):
    # Ensure timestamp is a string for JSON serialization
    return {
        "id": log.id,
        "plant_id": log.plant_id,
        "timestamp": str(log.timestamp), # Convert datetime object to string
        "humidity": log.humidity
    }

# --- API Endpoints ---

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the plant monitor API!"})

@app.route('/plants', methods=['GET'])
def get_plant_list():
    """Retrieves a list of all plants."""
    plants = Plant.get_all()
    return jsonify([plant_to_dict(p) for p in plants])

@app.route('/plants', methods=['POST'])
def create_plant():
    """Creates a new plant.
    Expected JSON: {"name": "Plant Name"}
    """
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing 'name' in request body"}), 400

    name = data['name']
    new_plant = Plant.add(name)
    if new_plant:
        return jsonify({"status": "created", "plant": plant_to_dict(new_plant)}), 201
    else:
        return jsonify({"error": f"Plant with name '{name}' already exists or could not be created"}), 409 # Conflict

@app.route('/plants/<int:plant_id>', methods=['GET'])
def get_plant_details(plant_id):
    """Retrieves details of a specific plant."""
    plant = Plant.get_by_id(plant_id)
    if plant:
        return jsonify(plant_to_dict(plant))
    else:
        return jsonify({"error": f"Plant with ID {plant_id} not found"}), 404

@app.route('/plants/<int:plant_id>', methods=['PUT'])
def update_plant_name(plant_id):
    """Updates a plant's name.
    Expected JSON: {"name": "New Plant Name"}
    """
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing 'name' in request body"}), 400

    new_name = data['name']
    if Plant.update(plant_id, new_name):
        updated_plant = Plant.get_by_id(plant_id) # Fetch updated plant to return current state
        return jsonify({"status": "updated", "plant": plant_to_dict(updated_plant)})
    else:
        return jsonify({"error": f"Plant with ID {plant_id} not found or could not be updated"}), 404

@app.route('/plants/<int:plant_id>', methods=['DELETE'])
def delete_plant(plant_id):
    """Deletes a plant and its associated humidity logs."""
    if Plant.delete(plant_id):
        return jsonify({"status": "deleted", "id": plant_id})
    else:
        return jsonify({"error": f"Plant with ID {plant_id} not found or could not be deleted"}), 404

@app.route('/plants/<int:plant_id>/humidity_logs', methods=['GET'])
def get_plant_humidity_logs(plant_id):
    """Retrieves humidity logs for a specific plant.
    Optional query parameter: 'limit' (e.g., /plants/1/humidity_logs?limit=5)
    """
    limit = request.args.get('limit', default=10, type=int) # Default to 10 logs
    humidity_logs = HumidityLog.get_latest_for_plant(plant_id, limit=limit)
    return jsonify([humidity_log_to_dict(log) for log in humidity_logs])

@app.route('/humidity_logs/latest_grouped', methods=['GET'])
def get_latest_humidity_for_each_plant():
    """Retrieves the latest humidity log for each plant, grouped by plant ID."""
    grouped_logs = HumidityLog.get_latest_logs_grouped_by_plant()
    # Convert logs within the dictionary to dicts for JSON serialization
    converted_grouped_logs = {
        plant_id: [humidity_log_to_dict(log) for log in logs]
        for plant_id, logs in grouped_logs.items()
    }
    return jsonify(converted_grouped_logs)


