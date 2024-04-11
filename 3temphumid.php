<?php
// Database configuration
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "sensor_data_db";

// Create a connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if the request method is POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get the data from the request
    $device_id = $_POST["device_id"];
    $temp = $_POST["temp"];
    $humid = $_POST["humid"];

    // Prepare an SQL statement to insert the data into a table
    $sql = "INSERT INTO sensor (device_id, temperature, humidity, created_at) VALUES ('$device_id', '$temp', '$humid', NOW())";

    // Execute the SQL statement
    if ($conn->query($sql) === TRUE) {
        echo "Data inserted successfully";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

// Close the connection
$conn->close();
?>
