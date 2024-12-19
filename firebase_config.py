import json

# Path to the Service Account JSON file
SERVICE_ACCOUNT_FILE = "config/service_account.json"

# Load the JSON credentials
def load_firebase_config():
    with open(SERVICE_ACCOUNT_FILE, "r") as file:
        config = json.load(file)
    return config

# Example function to extract a specific key (e.g., project_id)
def get_project_id():
    config = load_firebase_config()
    return config.get("project_id")
