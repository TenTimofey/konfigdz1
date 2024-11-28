import json
from datetime import datetime

class Logger:
    def __init__(self, log_path):
        self.log_path = log_path
        self.actions = []

    def log(self, action):
        self.actions.append({'timestamp': datetime.now().isoformat(), 'action': action})

    def save(self):
        with open(self.log_path, 'w') as log_file:
            json.dump(self.actions, log_file, indent=4)