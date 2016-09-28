<?php
include_once("../conf/globals.php");

$id = $_POST['id'];
$user = $_POST['user'];

$con = mysqli_connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, DB_NAME);

$remove_query = "DELETE FROM `hangouts` WHERE `id` = '".$id."' AND `organizer` = '".$user."'";
$result = mysqli_query($con, $remove_query);

mysqli_close($con);
?>

