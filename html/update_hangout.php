<?php
include_once("../conf/globals.php");

$id = $_POST['id'];
$user = $_POST['user'];
$going = $_POST['going'];
$notGoing = $_POST['notGoing'];

$con = mysqli_connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, DB_NAME);

if ($going == "1"){
	$update_query = "UPDATE `hangouts` SET `going` = CONCAT(`going`, IF(LENGTH(`going`), ',', ''), '".$user."') WHERE `id` = '".$id."'";
        $result = mysqli_query($con, $update_query);
        if ($result) {
		$update_query = "UPDATE `hangouts` SET `notgoing` = CASE WHEN `notgoing` LIKE '%,".$user."%' THEN REPLACE(`notgoing`, ',".$user."', '') WHEN `notgoing` LIKE '%".$user.",%' THEN REPLACE(`notgoing`, '".$user.",', '') WHEN `notgoing` LIKE '%$user%' THEN REPLACE(`notgoing`, '$user', '') ELSE NULL END WHERE `id` = '".$id."'";
                $result = mysqli_query($con, $update_query);
        }
}
elseif ($notGoing == "1") {
	$update_query = "UPDATE `hangouts` SET `notgoing` = CONCAT(`notgoing`, IF(LENGTH(`notgoing`), ',', ''), '".$user."') WHERE `id` = '".$id."'";
        $result = mysqli_query($con, $update_query);
        if ($result) {
		$update_query = "UPDATE `hangouts` SET `going` = CASE WHEN `going` LIKE '%,".$user."%' THEN REPLACE(`going`, ',".$user."', '') WHEN `going` LIKE '%".$user.",%' THEN REPLACE(`going`, '".$user.",', '') WHEN `going` LIKE '%$user%' THEN REPLACE(`going`, '$user', '') ELSE NULL END WHERE `id` = '".$id."'";
                $result = mysqli_query($con, $update_query);
        }
}

mysqli_close($con);
?>
