<!-- REMOVE BR AND STYLE THIS SHIT -->
<script type="text/javascript" src="<?php echo $linker->host() ?>/inc/js/form_validation.js"></script>

<?php 
	if(isset($_POST["signUpFormSubmitted"])){
		$formName = $conn->real_escape_string(htmlspecialchars($_POST["name"]));
		$formSurname = $conn->real_escape_string(htmlspecialchars($_POST["surname"]));
		$formEmail= filter_var($conn->real_escape_string(htmlspecialchars($_POST["email"])), FILTER_VALIDATE_EMAIL);
		$formLogin = $conn->real_escape_string(htmlspecialchars($_POST["login"]));	
		$formPassword = $conn->real_escape_string(htmlspecialchars($_POST["password"]));
		$formPasswordRep = $conn->real_escape_string(htmlspecialchars($_POST["repeatPassword"]));
		
		if(mysqli_fetch_row($conn->query("SELECT * FROM users where login ='".$formLogin."' LIMIT 1")))
		{
			$text->translate("loginTaken");
			return;
		}


		if(mysqli_fetch_row($conn->query("SELECT * FROM users where email ='".$formEmail."' LIMIT 1")))
		{
			$text->translate("mailTaken");
			return;
		}

		if(
		$formEmail &&
		mb_strlen($formName, 'UTF-8')>=2 &&
		mb_strlen($formName, 'UTF-8')<=30 &&
		mb_strlen($formSurname, 'UTF-8')>=2 &&
		mb_strlen($formSurname, 'UTF-8')<=50 &&
		mb_strlen($formEmail,'UTF-8') &&
		mb_strlen($formEmail,'UTF-8')<=50 &&
		mb_strlen($formLogin,'UTF-8')>=4 &&
		mb_strlen($formLogin,'UTF-8')<=25 &&
		mb_strlen($formPassword,'UTF-8')>=6 &&
		mb_strlen($formPassword,'UTF-8')<=200 &&
		mb_strlen($formPasswordRep, 'UTF-8')>=6 &&
		($formPassword === $formPasswordRep) &&
		preg_match('/^\p{L}(( |-)?\p{L})*$/u', $formName) &&
		preg_match('/^\p{L}(( |-)?\p{L})*$/u', $formSurname) &&
		preg_match('/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/',$formEmail) &&
		!preg_match('/[^a-zA-Z\d_\.-]/', $formLogin) &&
		preg_match('/^[a-zA-Z]((_|-|\.)?[a-zA-Z\d]+)*$/', $formLogin)){
		
			$hash = md5($formName.$formSurname.$formLogin.time());
			$about =json_encode( [ 'hash' => $hash, 'date' => date("Y-m-d")]) ;
			$hashedPassword = password_hash($formPassword,PASSWORD_DEFAULT);
			$query = $conn->prepare('INSERT INTO users (rank, email, name, surname, login, password, about) VALUES (3, ?, ?, ?, ?, ?, ?)');
			$query->bind_param('ssssss', $formEmail, $formName, $formSurname, $formLogin, $hashedPassword, $about);
			if($query->execute()){
				echo $_SERVER['SERVER_NAME']."/project/activate_account.php?user=".$formLogin."&hash=".$hash;
			}
			else
				$text->translate('accountCreationProblem');
		}
		else{
			echo $text->translate("fillFieldsCorrectly");
		}

		return;

	}

?>


<form method="POST" action="<?php $_SERVER['PHP_SELF']?>" 
onkeyup="validateForm(this.name.value, this.surname.value, this.email.value, this.login.value, this.password.value, this.repeatPassword.value )">
<input 
	id="createAccountFormName"
	type="text" 
	name="name" 
	value=""
	maxlength="30"
	onkeyup="validName(this.value, this.id,0)"
	onfocus="clearColorFromField(this.id,1)"
	onchange="validName(this.value, this.id,1)"
	onblur="validName(this.value, this.id,1)" 
	placeholder="<?php $text->translate("name") ?>"
> <br>

<input
	id="createAccountFormSurname"
	type="text" 
	name="surname"
	value=""
	maxlength="50"
	onkeyup="validName(this.value, this.id,0)"
	onfocus="clearColorFromField(this.id,1)"
	onchange="validName(this.value, this.id,1)"
	onblur="validName(this.value, this.id,1)" 
	placeholder="<?php $text->translate("surname") ?>"
> <br>

<input
	id="createAccountFormEmail"
	type="text" 
	name="email" 
	value=""
	maxlength="50"
	onkeyup="validEmail(this.value, this.id,0)"
	onchange="validEmail(this.value,this.id,1)" 
	onblur="validEmail(this.value,this.id,1)" 
	onfocus="clearColorFromField(this.id,1)"
	placeholder="<?php $text->translate("email") ?>"
><br>

<input 
	id="createAccountFormLogin"
	type="text" 
	name="login" 
	value=""
	maxlength="25"
	onkeydown="removeClassFromField('validFormField',this.id); createAccountFormLoginValid = false;"
	onkeyup="if (validLogin(this.value,this.id,0)) availableLogin(this.value, this.id, 0)"
	placeholder="<?php $text->translate("login") ?>"
	onfocus="clearColorFromField(this.id)"
	onblur="if (validLogin(this.value,this.id,1)) availableLogin(this.value, this.id, 1)"
	onchange="if (validLogin(this.value,this.id,1)) availableLogin(this.value, this.id, 1)"
><br>


	<input 
		id="createAccountFormPass"
		type="password"
		name="password"
		value=""
		maxlength="200"
		class="passwords"
		onkeyup="passwordsAreIdentical()"
		onkeydown="clearColorFromPasswords();"
		onchange="validPassword(this.value,this.id)"
		onblur="validPassword(this.value,this.id)"
		onfocus="clearColorFromField(this.id)"
		placeholder="<?php $text->translate("password") ?>"
	><br>


	<input 
		id="createAccountFormPassRepeated"
		type="password" 
		name="repeatPassword" 
		value=""
		maxlength="200"
		class="passwords"
		onkeyup="passwordsAreIdentical()"
		onkeydown="clearColorFromPasswords();"
		onchange="validPassword(this.value,this.id)"
		onblur="validPassword(this.value,this.id)"
		onfocus="clearColorFromField(this.id)"
		placeholder="<?php $text->translate("repeatPassword") ?>"
	><br>


<input 
	id="submitButton"
	name="signUpFormSubmitted"
	type="submit"
	value="<?php $text->translate("createAccount") ?>"
><br>


</form>








<!-- 
<hr>


<?php $text->translate("additionalInfo") ?><br>

<?php $text->translate("sex") ?><br>
<label><input type="radio" name="sex" value="man"> <?php $text->translate("man")?></label>
<label><input type="radio" name="sex" value="woman"> <?php $text->translate("woman")?></label>

<br>
<input
	 type="text"
	 name="dateOfBirth"
	 placeholder="<?php $text->translate("dateOfBirth") ?>"
 > <br>

<input 
	type="text" 
	name="height" 
	placeholder="<?php $text->translate("height") ?>"
><br>

<input 
type="text" 
name="weight" 
placeholder="<?php $text->translate("weight") ?>"
><br>

<label><input type="checkbox" name="stressWork"><?php $text->translate("stressWork") ?></label><br>
<label><input type="checkbox" name="compWork"><?php $text->translate("compWork") ?></label><br>
<label><input type="checkbox" name="pills"><?php $text->translate("pills") ?></label><br>
<label><input type="checkbox" name="pregnant"><?php $text->translate("pregnant") ?></label><br>



 -->


