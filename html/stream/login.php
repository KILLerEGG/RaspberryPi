<html>
  <?php
  session_start();
  if (isset($_SESSION['name'])){
    header("Location: index.php");
  }
  ?>
  <head>
  <title>Animalcam Login</title>
  <link type="text/css" rel="stylesheet" href="style.css" />
  </head>
  <body>
    <div id="loginform">
    <form action="index.php" method="post">
      <p>Please enter your name to continue:</p>
      <label for="name" name="name" id="name" />
      <input type="text" name="name" id="name" />
      <input type="submit" name="enter" id="enter" value="Enter" />
    </form>
    </div>
  </body>
</html>
