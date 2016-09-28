<?php
include_once("../conf/globals.php");

$id = $_GET['id'];

$con = mysqli_connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, DB_NAME);

if (mysqli_connect_errno())
        echo "Failed to connect to MySQL: " . mysqli_connect_error();

$search_hang = "SELECT * FROM `hangouts` WHERE `id` = '".$id."'";

if ($result_hang = mysqli_query($con, $search_hang)){
        $hangoutsArray = array();

        while ($row = $result_hang->fetch_object()){
                array_push($hangoutsArray, $row);
        }

        echo json_encode($hangoutsArray);
}

mysqli_close($con);
?>

