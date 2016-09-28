<?php
include_once("../conf/globals.php");

$con = mysqli_connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, DB_NAME);

if (mysqli_connect_errno())
	echo "Failed to connect to MySQL: " . mysqli_connect_error();

$search_gar = "SELECT * FROM `garage_users` ORDER BY `order` ASC";

if ($result_gar = mysqli_query($con, $search_gar)){
	$garageArray = array();

	while ($row = $result_gar->fetch_object()){
		array_push($garageArray, $row);
	}

	echo json_encode($garageArray);
}

mysqli_close($con);
?>
