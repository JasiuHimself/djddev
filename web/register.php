<?php

	error_reporting(-1);
	require_once("classes/text.php");
	require_once("classes/connection.php");
	require_once("classes/linker.php");
	require_once("classes/user_class.php");

	session_start();
	require_once("header.php");

	$text = new Text("pl");
	

	require_once("inc/register.php");

	require_once("footer.php");


?>

