import json
from bson import ObjectId

def prepare_for_json(data):
    """Convert ObjectId fields to strings for JSON serialization."""
    if isinstance(data, dict):
        return {k: prepare_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [prepare_for_json(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data

def json_serialize(data):
    """Serialize data to JSON, handling ObjectId conversion."""
    prepared_data = prepare_for_json(data)
    return json.dumps(prepared_data, ensure_ascii=False)