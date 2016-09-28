<?php
include_once("../conf/globals.php");

$id = $_POST['id'];
$location = $_POST['location'];
$seconds = $_POST['seconds'];
$address = $_POST['address'];

$con = mysqli_connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, DB_NAME);

$update_query = "UPDATE `hangouts` SET `location` = '".$location."', `address` = '".$address."', `seconds` = '".$seconds."' WHERE `id` = ".$id;
$query_result = mysqli_query($con, $update_query);

mysqli_close($con);
?>
