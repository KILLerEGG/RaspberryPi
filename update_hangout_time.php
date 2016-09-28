<?php
include_once("conf/globals.php");

$con = mysqli_connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, DB_NAME);

$update_query = "UPDATE `hangouts` SET `minutes` = `minutes` - 1 WHERE `minutes` >= 0";
$result = mysqli_query($con, $update_query);

mysqli_close($con);
?>
