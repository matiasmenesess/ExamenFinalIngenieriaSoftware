from flask import Flask, jsonify
from data_handler import DataHandler

app = Flask(__name__)
data_handler = DataHandler()

class TaskController:
    def __init__(self, data_handler):
        self.data_handler = data_handler

@app.route('/dummy', methods=['GET'])
def dummy_endpoint():
    # Example dummy response
    return jsonify({"message": "This is a dummy endpoint!"})

if __name__ == '__main__':
    app.run(debug=True)