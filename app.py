from flask import Flask, jsonify, request
from predict import predict_l33
app = Flask(__name__)

def authenticate(username, password):

    admins = {
        'sT8t5JJM': 'u2K%qW',
        'u2K': 'qWsT8t5JJM'
    }
    if username in admins and password == admins[username]:
        return True
    return False


class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add_to_head(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def remove_last(self):
        if not self.head or not self.head.next:
            return
        second_last = self.head
        while second_last.next.next:
            second_last = second_last.next
        second_last.next = None

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

@app.route("/")
def homepage():
    """
    Endpoint for homepage
    """
    return "Welcome to the REST API!"


@app.route('/predict_MB2p', methods=['POST'])
def predict():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not authenticate(username, password):
        return jsonify({"success": False, "message": "Authentication failed"})

    df, new_encoded_time, issue = predict_l33()
    pred_oddEven = df["correction_predict_oddEven"].iloc[0]
    consecutive_errors_oddEven = df["wrong_correction_oddEven"].iloc[0]

    pred_bigSmall = df["correction_predict_bigSmall"].iloc[0]
    consecutive_errors_bigSmall = df["wrong_correction_bigSmall"].iloc[0]

    even_odd_prediction = {
        "prediction": pred_oddEven,
        "wrong_predictions": str(consecutive_errors_oddEven),
    }
    big_small_prediction = {
        "prediction": pred_bigSmall,
        "wrong_predictions": str(consecutive_errors_bigSmall),
    }

    current_time = new_encoded_time

    response = {
        "success": True,
        "issue": str(issue),
        "predict": {
            "even_odd": even_odd_prediction,
            "big_small": big_small_prediction
        },
        "point": {
            "even_odd": "0",
            "big_small": "0"
        },
        "time": str(current_time)
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
    