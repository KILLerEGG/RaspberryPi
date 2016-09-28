<?php
include_once("conf/globals.php");

$garageArray = array();
$inGarage = array();
$hasPass = 0;

$con = mysqli_connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, DB_NAME);

$search_gar = "SELECT * FROM `garage_users` ORDER BY `order` ASC";
$result_gar = mysqli_query($con, $search_gar);

while($row = mysqli_fetch_array($result_gar)){
        $name    = $row['name'];
        $garage  = $row['garage'];
        $outside = $row['outside'];
        $pass    = $row['pass'];
        $order   = $row['order'];

        $garageArray[$name] = array(
                                "garage"  => $garage,
                                "outside" => $outside,
                                "pass"    => $pass,
                                "order"   => $order
                              );
}

$numUsers = sizeof($garageArray);

function getCurrentWeek(){
        global $inGarage;
        global $garageArray;
        global $numUsers;
	global $hasPass;
	global $con;

        foreach ($garageArray as $user => $values){
                if ($values["garage"] === "1")
                        array_push($inGarage, (int)$values["order"]);

                if ($values["pass"] === "1")
                        $hasPass = (int)$values["order"];
        }
}

function updateGarage(){
        global $inGarage;
        global $garageArray;
        global $numUsers;
	global $hasPass;
	global $con;

	$newGarage = array();
	$newOutside = array();
	$newPass = "";

        $inGarage_it1 = ($inGarage[0] + 2) % $numUsers;
        $inGarage_it2 = ($inGarage[1] + 2) % $numUsers;
        $pass_it = ($hasPass + 2) % $numUsers;

        foreach ($garageArray as $user => $values){
                if ((int)$values["order"] === $inGarage_it1)
			array_push($newGarage, $user);
                elseif ((int)$values["order"] === $inGarage_it2)
                        array_push($newGarage, $user);
		elseif ((int)$values["order"] === $pass_it)
			$newPass = $user;
		else
			array_push($newOutside, $user);
        }
	$newGarageQuery = "UPDATE `garage_users` SET `garage`='1', `outside`='0', `pass`='0' WHERE `name`='".$newGarage[0]."' OR `name`='".$newGarage[1]."'";
	$newPassQuery = "UPDATE `garage_users` SET `garage`='0', `pass`='1', `outside`='1' WHERE `name`='".$newPass."'";
	$newOutsideQuery = "UPDATE `garage_users` SET `garage`='0', `pass`='0', `outside`='1' WHERE `name`='".$newOutside[0]."' OR `name`='".$newOutside[1]."'";

	$result_gar = mysqli_query($con, $newGarageQuery);
	$result_pass = mysqli_query($con, $newPassQuery);
	$result_out = mysqli_query($con, $newOutsideQuery);
}

getCurrentWeek();
updateGarage();

mysqli_close($con);
?>
