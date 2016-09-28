<?php
session_start();
//date_default_timezone_set('UTC');
if (isset($_SESSION['name'])){
  //$timezone = new DateTimeZone('America/Los_Angeles');
  //$datetime = new DateTime('now', $timezone);
  //$timestamp = $datetime->format('g:i A');
  $text = $_POST['text'];
  //file_put_contents("log.html", "<div class='msgln'>(".date("g:i A").") <b>".$_SESSION['name']."</b>: ".stripslashes(htmlspecialchars($text))."<br></div>", FILE_APPEND);
  //$last_post = new DateTime(strtotime(filemtime("log.html")), $timezone);
  $last_post = date('Ymd', filemtime("log.html"));
  //$last_modified =  (integer)$last_post->format('d'); 
  //$today = (integer)$datetime->format('d');
  $fp = fopen("log.html", 'a');
  if (date('Ymd') != $last_post){
    fwrite($fp, "<div style='text-align:center;' class='msgln'><i>".date('n/j/Y')."</i><br></div>");
  }
  fwrite($fp, "<div class='msgln'>(".date('g:i A').") <b>".$_SESSION['name']."</b>: ".stripslashes(htmlspecialchars($text))."<br></div>");
  fclose($fp);
}
?>
