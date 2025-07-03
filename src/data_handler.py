import json


class DataHandler:
    def __init__(self, filename='data.json'):
        self.filename = filename
        self.tasks = []
        self.users = []
        self.load_data()

    def save_data(self):
        data = {
            'tasks': self.tasks,
            'users': self.users
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.tasks = data.get('tasks', [])
                self.users = data.get('users', [])
        except FileNotFoundError:
            self.tasks = []
            self.users = []