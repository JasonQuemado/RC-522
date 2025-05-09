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
    //Cambiamos esta función siguiendo las instrucciones del profesor
    //Y quitamos todo lo de gt, lt...
    if (!is_array($value)) {
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
//Añadimos el ordenamiento de las tablas en el servidor,
//de todos modos habrá que hacer algo en el cliente de todos modos
/*} elseif ($table === 'timetables') {
    $sql .= " ORDER BY FIELD(day, 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'), hour ASC";
}*/
//ha habido que poner lo de today ya que no se hacñia correctamente,
//desde el cliente pondremos como parámetro el día de hoy
} elseif ($table === 'timetables' && isset($params['today'])) {
    $day = $conn->real_escape_string($params['today']);
    $dias = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    $orden = [];

    $start = array_search($day, $dias);
    for ($i = 0; $i < 7; $i++) {
        $orden[] = "'" . $dias[($start + $i) % 7] . "'";
    }
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
