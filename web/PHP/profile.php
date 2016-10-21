
<?php

	error_reporting(-1);
	require_once("classes/text.php");
	require_once("classes/connection.php");
	require_once("classes/linker.php");
	require_once("classes/user_class.php");

	session_start();
	//require_once("header.php");


	$text = new Text("pl");


	$user->myProfile($text, $conn);

?>
<!-- wyjeb -->
<link rel="stylesheet" type="text/css" href="<?php echo $linker->host() ?>/inc/style.css" />

<div id="calendar"></div>

<script type="text/javascript" src=<?php echo $linker->host() ?>/inc/js/calendar.js></script>




<?php
	require_once("footer.php");
?>
