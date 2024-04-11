import requests

url = 'http://localhost:5000/post-data'  # Replace 'localhost' with your server's IP or hostname if necessary
data = {
    'device_id': 'M1D2',
    'temperature': 25.5,
    'humidity': 60,

}

response = requests.post(url, data=data)

print(response.text)
