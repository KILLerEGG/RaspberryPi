<?php

/*
 ********************************
 * garage.php			*
 *				*
 * Written by: Graham Turbyne	*
 * Date: 7/25/2016		*
 ********************************
*/

// Include the global values, but make them unaccessible to anyone not logged into the pi
include_once("../conf/globals.php");

define('WEEK_START', 1); //[0-6] -> 1=Monday, 2=Tuesday, ...

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

function week_bounds($date){
	$date = strtotime($date);
	$start = $date;

	//Find beginning day of week (defined by WEEK_START)
	while(date('w', $start) > WEEK_START){
		$start -= 86400; //One day
	}
	//Add 6 days to the start to get your end
	$end = date('n/j/Y', $start + (6 * 86400));
	$start = date('n/j/Y', $start);
	//Display the week range
	echo '<i>'.$start.'</i> - <i>'.$end.'</i>';
}

//Initializes global variables. This function should always be called before other 'week' functions
function establishCurrentWeek(){
	global $inGarage;
        global $garageArray;
        global $numUsers;
        global $hasPass;

        foreach ($garageArray as $user => $values){
                if ($values["garage"] === "1")
                        array_push($inGarage, (int)$values["order"]);
        }
        foreach ($garageArray as $user => $values){
                if ($values["pass"] === "1")
                        $hasPass = (int)$values["order"];
        }
}

function getCurrentWeek(){
	global $inGarage;
	global $garageArray;
	global $numUsers;
	global $hasPass;
	global $globalPicsArray;

	echo '<h2>Garage:</h2>';
	echo '<ul>';
	foreach ($garageArray as $user => $values){
        	if ($values["garage"] === "1"){
			echo '<li>';
			echo '<img src="http://graph.facebook.com/'.$globalPicsArray[$user].'/picture?type=large&width=100&height=100" />';
                	echo '<h3>'.$user.'</h3>';
			echo '</li>';
		}
	}
	echo '</ul>';
	echo '<h2>Pass:</h2>';
	echo '<ul>';
	foreach ($garageArray as $user => $values){
		if ($values["pass"] === "1"){
                        echo '<li>';
			echo '<img src="http://graph.facebook.com/'.$globalPicsArray[$user].'/picture?type=large&width=100&height=100" />';
                        echo '<h3>'.$user.'</h3>';
			echo '</li>';
		}
        }
	echo '</ul>';
}

function getPrevWeek($numWeeks){
	global $inGarage;
        global $garageArray;
        global $numUsers;
        global $hasPass;
	global $globalPicsArray;

        $weekAddition = (2 * $numWeeks) * -1;
        $inGarage_it1 = (($inGarage[0] % $numUsers) + $weekAddition) % $numUsers;
	if ($inGarage_it1 < 0)
		$inGarage_it1 = $inGarage_it1 + $numUsers;
        $inGarage_it2 = (($inGarage[1] % $numUsers) + $weekAddition) % $numUsers;
	if ($inGarage_it2 < 0)
                $inGarage_it2 = $inGarage_it2 + $numUsers;
        $pass_it = (($hasPass % $numUsers) + $weekAddition) % $numUsers;
	if ($pass_it < 0)
                $pass_it = $pass_it + $numUsers;
        echo '<h2>Garage:</h2>';
	echo '<ul>';
        foreach ($garageArray as $user => $values){
                if ((int)$values["order"] === $inGarage_it1){
                        echo '<li>';
			echo '<img src="http://graph.facebook.com/'.$globalPicsArray[$user].'/picture?type=large&width=100&height=100" />';
			echo '<h3>'.$user.'</h3>';
			echo '</li>';
		}
                elseif ((int)$values["order"] === $inGarage_it2){
                        echo '<li>';
                        echo '<img src="http://graph.facebook.com/'.$globalPicsArray[$user].'/picture?type=large&width=100&height=100" />';
                        echo '<h3>'.$user.'</h3>';
                        echo '</li>';
		}
        }
	echo '</ul>';
	echo '<h2>Pass:</h2>';
	echo '<ul>';
        foreach ($garageArray as $user => $values){
                if ((int)$values["order"] === $pass_it){
			echo '<li>';
                        echo '<img src="http://graph.facebook.com/'.$globalPicsArray[$user].'/picture?type=large&width=100&height=100" />';
                        echo '<h3>'.$user.'</h3>';
                        echo '</li>';
		}
        }
	echo '</ul>';
}

function getFutureWeek($numWeeks){
	global $inGarage;
	global $garageArray;
	global $numUsers;
	global $hasPass;
	global $globalPicsArray;

	$weekAddition = 2 * $numWeeks;
	$inGarage_it1 = ($inGarage[0] + $weekAddition) % $numUsers;
	$inGarage_it2 = ($inGarage[1] + $weekAddition) % $numUsers;
	$pass_it = ($hasPass + $weekAddition) % $numUsers;

	echo '<h2>Garage:</h2>';
	echo '<ul>';
	foreach ($garageArray as $user => $values){
		if ((int)$values["order"] === $inGarage_it1){
			echo '<li>';
                        echo '<img src="http://graph.facebook.com/'.$globalPicsArray[$user].'/picture?type=large&width=100&height=100" />';
                        echo '<h3>'.$user.'</h3>';
                        echo '</li>';
		}
		elseif ((int)$values["order"] === $inGarage_it2){
			echo '<li>';
                        echo '<img src="http://graph.facebook.com/'.$globalPicsArray[$user].'/picture?type=large&width=100&height=100" />';
                        echo '<h3>'.$user.'</h3>';
                        echo '</li>';
		}
	}
	echo '</ul>';
	echo '<h2>Pass:</h2>';
	echo '<ul>';
	foreach ($garageArray as $user => $values){
		if ((int)$values["order"] === $pass_it){
			echo '<li>';
                        echo '<img src="http://graph.facebook.com/'.$globalPicsArray[$user].'/picture?type=large&width=100&height=100" />';
                        echo '<h3>'.$user.'</h3>';
                        echo '</li>';
		}
	}
	echo '</ul>';
}

//Initialize global variables
establishCurrentWeek()

?>
<html>
  <head>
    <title>Team Grayson Garage</title>
    <link rel='stylesheet' type='text/css' href='css/garage.css'>
  </head>
  <body>
    <div style="width:100%;height:100%;display:flex;align-items:center">
      <div class="li_div" style="float:left;width:33.2%;text-align:center;"><h1>Previous Week:</h1><?php week_bounds("last monday");getPrevWeek(1);?></div>
      <div class="li_div" style="float:left;width:33.2%;text-align:center;"><h1>Current Week:</h1><?php week_bounds("now");getCurrentWeek();?></div>
      <div class="li_div" style="float:left;width:33.2%;text-align:center;"><h1>Next Week:</h1><?php week_bounds("next monday");getFutureWeek(1);?></div>
    </div>
  </body>
</html>
