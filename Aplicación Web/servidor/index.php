<?php 
require_once('configurador_php_sql.php'); $uid = $_POST['uid'] ?? '';
$name = $_POST['name'] ?? '';
$consulta = $_POST['consulta'] ?? ''; $valid = false;

if ($uid && $name) {
  $stmt_check = $conn->prepare("SELECT * FROM students WHERE student_id = ? AND name = ?"); $stmt_check->bind_param("ss", $uid, $name);
  $stmt_check->execute();
  $result_check = $stmt_check->get_result();
  if ($result_check->num_rows > 0) {
    $valid = true;
  }
  $stmt_check->close(); 
}
?>
  
<!DOCTYPE html> <html lang="ca"> <head>
<meta charset="UTF-8">
<title>Client Web Course Manager</title> <link rel="stylesheet" href="style.css">
</head> <body>
