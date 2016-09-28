<?php
include_once("../conf/globals.php");

$organizer = $_POST['organizer'];
$location = $_POST['location'];
$seconds = $_POST['seconds'];
$address = $_POST['address'];

if (empty($address)){
        $address = "";
}

if (!empty($organizer) && !empty($location) && !empty($seconds)) {
        $con = mysqli_connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, DB_NAME);

        $insert_query = "INSERT INTO `hangouts` (`id`, `organizer`, `going`, `notgoing`, `location`, `address`, `seconds`) VALUES (NULL, '".$organizer."', '".$organizer."', '', '".$location."', '".$address."', '".$seconds."')";
        $query_result = mysqli_query($con, $insert_query);

        mysqli_close($con);
}
?>
