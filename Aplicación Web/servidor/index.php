<?php
require_once('configurador_php_sql.php');
$uid = $_POST['uid'] ?? '';
$name = $_POST['name'] ?? '';
$consulta = $_POST['consulta'] ?? '';
$valid = false;

if ($uid && $name) {
  $stmt_check = $conn->prepare("SELECT * FROM students WHERE student_id = ? AND name = ?");
  $stmt_check->bind_param("ss", $uid, $name);
  $stmt_check->execute();
  $result_check = $stmt_check->get_result();
  if ($result_check->num_rows > 0) {
    $valid = true;
  }
  $stmt_check->close();
}
?>

<!DOCTYPE html>
<html lang="ca">
<head>
  <meta charset="UTF-8">
  <title>Client Web Course Manager</title>
  <link rel="stylesheet" href="style.css?v=2">

</head>
<body>
  <h1>Inici de sessió</h1>
  <form method="POST">
    <label>Nom:</label><input type="text" name="name" required><br>
    <label>UID:</label><input type="text" name="uid" required><br>
    <button type="submit" name="login">Entrar</button>
  </form>

<?php if ($uid && $name && !$valid): ?>
  <p style="color:red;">⚠️ Alumne no trobat. Comprova el nom i UID.</p>
<?php endif; ?>

<?php if ($valid): ?>
  <div>
    <h2>Consulta:</h2>
    <form method="POST">
      <input type="hidden" name="uid" value="<?php echo htmlspecialchars($uid); ?>">
      <input type="hidden" name="name" value="<?php echo htmlspecialchars($name); ?>">
      <button type="submit" name="consulta" value="timetables">Horaris</button>
      <button type="submit" name="consulta" value="tasks">Treballs</button>
      <button type="submit" name="consulta" value="marks">Notes</button>
    </form>
  </div>
<?php endif; ?>

<?php
if ($consulta && $valid) {
  if ($consulta === 'marks') {
    $query = "SELECT * FROM marks WHERE student_id = ?";
    $stmt = $conn->prepare($query);
    $stmt->bind_param("s", $uid);
  } elseif (in_array($consulta, ['timetables', 'tasks'])) {
    $query = "SELECT * FROM $consulta";
    $stmt = $conn->prepare($query);
  } else {
    echo "<p>Consulta no vàlida.</p>";
    exit;
  }

  $stmt->execute();
  $result = $stmt->get_result();

  if ($result->num_rows > 0) {
    echo "<table border='1' cellpadding='6' cellspacing='0' style='margin: auto; border-collapse: collapse;'>";
    echo "<thead><tr>";
    $row = $result->fetch_assoc();
    foreach ($row as $key => $value) {
      if ($key !== 'id' && $key !== 'student_id') {
        echo "<th>$key</th>";
      }
    }
    echo "</tr></thead><tbody>";
    do {
      echo "<tr>";
      foreach ($row as $key => $value) {
        if ($key !== 'id' && $key !== 'student_id') {
          echo "<td>$value</td>";
        }
      }
      echo "</tr>";
    } while ($row = $result->fetch_assoc());
    echo "</tbody></table>";
  } else {
    echo "<p>No hi ha dades.</p>";
  }
  $stmt->close();
  $conn->close();
}
?>
</body>
</html>
