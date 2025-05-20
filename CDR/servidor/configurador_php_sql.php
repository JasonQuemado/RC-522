<?php
$host = 'localhost';
$user = 'root';
$pass = '1234';
$db = 'atenea';

$conn = new mysqli($host, $user, $pass, $db);

if ($conn->connect_error) {
    die('Connection failed: ' . $conn->connect_error);
}
?>
