<?php
 /**
 * This class is impoementend in order to translate pages content
 */
 class Text
 {
 	private $language;
 	
 	function __construct($language)
 	{
 		$fileName = "lang/".$language.".json";
 		$languageHandle = fopen($fileName,'r');
		$languageContentsJSON = fread($languageHandle, filesize($fileName));
		$this->language = json_decode($languageContentsJSON,true);
		fclose($languageHandle);
		//$this->translateToJavaScipt($language);
 	}


 	function translate($word)
 	{
 		echo $this->language[$word];	
 	}

 	function insert($word)
 	{
 		return $this->language[$word];	
 	}



 	function translateToJavaScipt($language){
		echo 
		"<script>
			var languageData;
			$.getJSON(\"lang/".$language.".json\", function(data) {
	    	languageData = data;
		});
		</script>";
	}

 
 }




?>
