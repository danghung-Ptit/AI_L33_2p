import requests
import time

API_URL = 'http://0.0.0.0:9000/predict_MB2p'

username = 'sT8t5JJM'
password = 'u2K%qW'

while True:
    response = requests.post(API_URL, json={'username': username, 'password': password})

    if response.status_code == 200:
        print('Đăng nhập thành công!')
    else:
        print('Đăng nhập thất bại. Vui lòng kiểm tra lại thông tin đăng nhập.')

    print(response.text)
    time.sleep(120)
