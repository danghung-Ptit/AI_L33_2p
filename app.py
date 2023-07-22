from flask import Flask, jsonify, request
from predict import predict_big_small
app = Flask(__name__)

# Phần xác thực: kiểm tra thông tin đăng nhập
def authenticate(username, password):
    # Kiểm tra thông tin đăng nhập
    admins = {
        'sT8t5JJM': 'u2K%qW',
        'u2K': 'qWsT8t5JJM'
    }
    if username in admins and password == admins[username]:
        return True
    return False


def calculate_consecutive_errors(y_true, y_pred):
    consecutive_errors = 0
    for true, pred in zip(y_true, y_pred[1:]):
        true_label = true
        pred_label = pred
        if true_label != pred_label:
            consecutive_errors += 1

        else:
            break

    return consecutive_errors


@app.route("/")
def homepage():
    """
    Endpoint for homepage
    """
    return "Welcome to the REST API!"

@app.route('/predict_MB2p', methods=['POST'])
def predict():
    # Lấy thông tin đăng nhập từ body của request
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Kiểm tra thông tin đăng nhập
    if not authenticate(username, password):
        return jsonify({"success": False, "message": "Authentication failed"})

    y_pred_bigSmall, y_true_bigSmall, y_pred_oddEven, y_true_oddEven, new_encoded_time, issue = predict_big_small()

    # print("bigSmall")
    # print(y_true_bigSmall)
    # print(y_pred_bigSmall)
    #
    # print("oddEven")
    # print(y_true_oddEven)
    # print(y_pred_oddEven)
    # print("\n")

    consecutive_errors_bigSmall = calculate_consecutive_errors(y_true_bigSmall, y_pred_bigSmall)
    consecutive_errors_oddEven = calculate_consecutive_errors(y_true_oddEven, y_pred_oddEven)
    if y_pred_oddEven[0][0] == 1:
        pred_oddEven = "Odd"
    elif y_pred_oddEven[0][0] == 0:
        pred_oddEven = "Even"

    if y_pred_bigSmall[0][0] == 1:
        pred_bigSmall = "Big"
    elif y_pred_bigSmall[0][0] == 0:
        pred_bigSmall = "Small"


    # Mô phỏng dữ liệu dự đoán
    even_odd_prediction = {
        "prediction": pred_oddEven,
        "wrong_predictions": consecutive_errors_oddEven
    }
    big_small_prediction = {
        "prediction": pred_bigSmall,
        "wrong_predictions": consecutive_errors_bigSmall
    }

    current_time = new_encoded_time

    # Tạo đối tượng response JSON
    response = {
        "success": True,
        "issue": str(issue),
        "predict": {
            "even_odd": even_odd_prediction,
            "big_small": big_small_prediction
        },
        "time": str(current_time)
    }
    print(response)

    # Trả về response JSON
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
    