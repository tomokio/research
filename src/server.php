<?php
$uploaddir = '';
$file = basename($_FILES['uploadedfile']['name']);
$uploadfile = $uploaddir . $file;
echo "file=".$file; //is empty, but shouldn't
if (move_uploaded_file($_FILES['uploadedfile']['tmp_name'], $uploadfile)) {
	echo $file;
}
else {
	echo "error";
}
?>
