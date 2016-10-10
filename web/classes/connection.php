<?php
	$host = "localhost";
	$user = "root";
	$pass = "";
	$db = "project";
	$conn = new mysqli($host,$user,$pass,$db) or die("Error " . mysqli_error($link)); 
	$conn->query("SET NAMES UTF8");


?>
