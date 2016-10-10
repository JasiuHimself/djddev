<?php


 class Linker{ // tymczasowy ??
	var $index;	
	var $register;
	public static function host() {
		$link = pathinfo($_SERVER['SCRIPT_NAME']);
		if($link['dirname'] == '/') $link['dirname'] = NULL;
		return 'http://'.$_SERVER['HTTP_HOST'].$link['dirname'];
	}

	function __construct() {
		$this->index = $this->host();
		$this->register = $this->index.'/register/';
	}

}

//echo Linker::host().'/';
$linker = new Linker();

?>