import json

def convert_to_json(id, reading):
    # Create a dictionary
    data = {
        "id": id,
        "time": reading.get_time(),
        "usage": reading.get_usage()
    }
    # Convert the dictionary to a JSON string
    json_object = json.dumps(data, indent=4)
    # Convert the json string to JSON object
    json_object = json.loads(json_object)
    return json_object