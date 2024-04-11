from flask import Flask, request
import mysql.connector
import datetime

app = Flask(__name__)

# MySQL connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'sensor_data_db'
}

@app.route('/post-data', methods=['POST'])
def post_data():
    # Connect to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Get data from the POST request
    location = request.form['device_id']
    temp = request.form['temperature']
    humid = request.form['humidity']
    created_at = datetime.datetime.now()

    # Insert data into the database
    query = "INSERT INTO sensor (device_id, temperature, humidity, created_at) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (location, temp, humid, created_at))
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

    return 'Data received and stored successfully'

if __name__ == '__main__':
    app.run(debug=True)
