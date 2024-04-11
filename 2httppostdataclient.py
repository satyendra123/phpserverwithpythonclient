import requests

url = 'http://127.0.0.1:5000/validate'  # Update the URL if your Flask server is running on a different address
data = {
    'did': 'S2M1D1',
    'qrcde': '2603109015000200001423'
}

response = requests.post(url, json=data)
print(response.json())
