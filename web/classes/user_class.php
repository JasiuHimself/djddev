<?php


class UserClass
{


	function verifyUser($text, $conn, $login, $pass, $redirect=NULL){
		$sanitizedLogin = $conn->real_escape_string(htmlspecialchars($login));
		$sanitizedPassword = $conn->real_escape_string(htmlspecialchars($pass));
		
		$stmt = $conn->prepare('SELECT * from users WHERE login=? LIMIT 1');
		$stmt->bind_param('s', $sanitizedLogin);
		$stmt->execute();
		$res = $stmt->get_result();
		$fetchedArray = $res->fetch_assoc();

		//two cases 1=validate password, 2-validate if user is active and not banned, when password =0
		if ($fetchedArray){
			if (password_verify($sanitizedPassword,$fetchedArray['password'])){
				if ($fetchedArray['rank'] == 3) {
					if ($redirect)	header('Location: '.Linker::host().'/inactive.php');			
					return false;
				}
				else return true;
			}
			else return false;
		}
		else
			return false;
		
	}

	
	function logging($text, $conn){

		if (isset($_POST['signin'])){
			if (isset($_POST['login']) && isset($_POST['password']))
				if($_POST['login']!= "" && $_POST['password']!=""){
					if ($this->verifyUser($text, $conn,$_POST['login'],$_POST['password'],1)){
							$_SESSION['login'] = $conn->real_escape_string(htmlspecialchars($_POST['login']));
							$this->userTools($text,$conn);
							return;
					}else
						$text->translate('invalidCredentials');

				}else
					$text->translate('fillFieldsCorrectly');
		}else
			$this->loggingForm($text);

	}
	
	function loggingForm($text)
	{
		echo 
		'<form method="POST">
			<input type="text" name="login" placeholder="'.$text->insert("login").'">
			<input type="password" name="password" placeholder="'.$text->insert("password").'">
			<input type="submit" name="signin" value="'.$text->insert("signIn").'">
			<label><input type="checkbox" name="rememberMe" >'.$text->insert("rememberMe").'</label>
		</form>

		<a href="register/" >'.$text->insert("createAccount").'</a>';
	}


	function userTools($text,$conn)
	{
		if (isset($_GET['logout'])){
			$this->logOut();
		}

		if (isset($_SESSION['login'])){
			echo '<a href="profile"> Profile</a>';								
			echo '<a href="logout"> Logout</a>';
		}
		else
			$this->logging($text,$conn);
	}

	function logOut(){
			session_unset();  
			session_destroy(); 
			unset($_GET['logout']);
			header( "Location: /");
	}

	function activateAccount($text,$conn)
	{
		if(isset($_GET["user"]) && isset($_GET["hash"])){
			$userActivation = $conn->real_escape_string(htmlspecialchars($_GET["user"]));
			$hashActivation = $conn->real_escape_string(htmlspecialchars($_GET["hash"]));
			if($result = mysqli_fetch_assoc($conn->query("SELECT * FROM users where login ='".$userActivation."' LIMIT 1")))
			{
				if ($result["rank"] == 3){				
					$resultJSON = json_decode($result["about"],true);
					if ($resultJSON["hash"] === $hashActivation){
						if ($conn->query("UPDATE users set rank=2, about='' WHERE login='".$userActivation."'"))
							$text->translate("activationSuccessful");
					}
				}else{
					$text->translate("alreadyActive");
				}
			}else
				$text->translate("noSuchUser");

		}
		else
			//header($_SERVER["SERVER_NAME"]); //if link is incorrect ->main page
		header( "Location: /"); //if action performed wait for the user to read info

		}


	function myProfile($text, $conn)
	{
		if(isset($_SESSION['login']))
		{
			$sessionLogin = $conn->real_escape_string(htmlspecialchars($_SESSION["login"]));
			$stmt = $conn->prepare('SELECT * from users WHERE login=? LIMIT 1');
			$stmt->bind_param('s', $sessionLogin);
			$stmt->execute();
			$res = $stmt->get_result();
			$row = $res->fetch_assoc();
			// if ($row)
			//  	var_dump($row);
			// else{
			// 	session_unset();  
			// 	session_destroy(); 
			// 	header( "Location: /");
			// }
			
			$conn->close();
		}else
			echo "false"; //sth went wrong
				
	}


}





 $user = new UserClass();








?>