# EXAMPLE-1 isme hum data send kar rhe hai apne php file ko. same chiz actually hum postman se bhi kar sakte hai. lekin hum yaha par is python ka code likhkar bana rhe hai
import requests

# URL of the server API endpoint
url = 'http://localhost/pythonclient/pythondata.php' # ye port 80 par run ho rha hai isliye hume likhne ki jarurat nahi hai lekin agar ye port 8080 par run hota to hume port likhne ki jarurat padhti kuch is tarah se 
#url = 'http://localhost:8080/pythonclient/pythondata.php'  agar to mera apache server 8080 port par run ho rha hota

data = {
    'device_id': 's2M1D1',
    'temperature': '29',
    'humidity': '35'
}
response = requests.post(url, data=data)
print(response.text)

'''
import requests
import json

url = 'http://localhost/pythonclient/qrdata.php'

# Card data to be sent
data = {
    'cid': '0698069871007110000008'  # Make sure this key is present
}

# Convert data to JSON format
json_data = json.dumps(data)

# Set the content type header to JSON
headers = {'Content-Type': 'application/json'}

# Send POST request to PHP server
response = requests.post(url, headers=headers, data=json_data)

# Print the response from the PHP server
print(response.json())
'''

'''
#EXAMPLE-3 is code me hum parally data send kar rhe hai apne load ko test krne ke liye. so isme mai direct 5 data send karuna ek hi time me ki ye work kar rha hai yaa nahi. hum apne server ka load test kar rhe hai ki agar ek sath itna sara data aayea to mera server kaise behave karega
import requests
import json
import concurrent.futures

url = 'http://localhost/pythonclient/qrdata.php'

card = ['0698069871007110000008', '0698069871007110000009', '0698069871007110000010', '0698069871007110000011', '0698069871007110000012']

def send_data(card):
    data = {
        'cid': card
    }

    json_data = json.dumps(data)
    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
    print(response.text)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(send_data, card)
'''


#EXAMPLE-4 is code me hum parally data send kar rhe hai apne load ko test krne ke liye. so isme mai excel se data uthata jaunga aur server par send karta jaunga test krne ke liye. actually hum aisa karke apne server ka load test kar rhe hai
'''
import requests
import json
import concurrent.futures

url = 'http://localhost/pythonclient/qrdata.php'

card = ['0698069871007110000008', '0698069871007110000009', '0698069871007110000010', '0698069871007110000011', '0698069871007110000012']

def send_data(card):
    data = {
        'cid': card
    }

    json_data = json.dumps(data)
    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})
    print(response.text)

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(send_data, card)
'''