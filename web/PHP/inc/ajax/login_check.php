<?php
	
	require_once("../../classes/connection.php");
	

	if (isset ($_POST['login'])){
		$formLoginAjax = $conn->real_escape_string(htmlspecialchars($_POST["login"]));
		$stmt = $conn->prepare('SELECT * from users WHERE login=? LIMIT 1');
		$stmt->bind_param('s', $formLoginAjax);
		$stmt->execute();
		$res = $stmt->get_result();
		$row = $res->fetch_assoc();
		if ($row)
		 	echo "false"; //login already in use
		else
		 	echo "true"; //login valid
		 $conn->close();
	}else
		echo "false"; //sth went wrong

?>
