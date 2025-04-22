<?php
require_once 'configurador_php_sql.php';

//Obtener la tabla desde la URL
//$request_uri = explode("/", $_SERVER['REQUEST_URI']);
//$table = isset($request_uri[1]) ? $request_uri[1] : '';
$table = basename(parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$query_string = $_SERVER['QUERY_STRING'] ?? '';

parse_str($query_string, $params);

//Aqui construimos la consulta SQL
$sql = "SELECT * FROM $table";
$conditions = [];

foreach ($params as $key => $value) {
    if (preg_match('/(.+)\[(.+)\]/', $key, $matches)) {
        $col = $matches[1];
        $op = $matches[2];
        $sql_op = match($op) {
            'gt' => '>',
            'lt' => '<',
            'gte' => '>=',
            'lte' => '<=',
            default => '='
        };
        $conditions[] = "$col $sql_op '" . $conn->real_escape_string($value) . "'";
    } elseif (!is_array($value) && $key !== 'limit') {
        $conditions[] = "$key = '" . $conn->real_escape_string($value) . "'";
    }
}

if (!empty($conditions)) {
    $sql .= " WHERE " . implode(" AND ", $conditions);
}

if ($table === 'tasks') {
    $sql .= " ORDER BY date ASC";
} elseif ($table === 'marks') {
    $sql .= " ORDER BY subject ASC";
} elseif ($table === 'students') {
    $sql .= " ORDER BY surname ASC";
}

if (isset($params['limit'])) {
    $sql .= " LIMIT " . intval($params['limit']);
}

$result = $conn->query($sql);
$data = [];

if ($result) {
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
} else {
    http_response_code(400);
    $data = ["error" => $conn->error];
}

header('Content-Type: application/json');
echo json_encode($data);
?>