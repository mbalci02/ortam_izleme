<?php 
//http://stackoverflow.com/a/2467974
$servername = "localhost";
$username = "root";
$password = "*******";
$dbname = "Ortam_Izleme";

// Create connection
$mysqli = new mysqli($servername, $username, $password, $dbname);

$query="SELECT ZAMAN2,PARLAKLIK FROM Kayitli_Olcumler"; 
$result=$mysqli->query($query)
	or die ($mysqli->error);

//store the entire response
$response = array();

//the array that will hold the titles and links
$posts = array();
while($row=$result->fetch_assoc()) //mysql_fetch_array($sql)
{ 
$ZAMAN2=$row['ZAMAN2']; 
$PARLAKLIK=$row['PARLAKLIK']; 

//each item from the rows go in their respective vars and into the posts array
$posts[] = array($ZAMAN2*1000,$PARLAKLIK*1); 
} 

//the posts array goes into the response
$response = $posts;
//echo "<h1>" . $posts . "</h1>";

//creates the file
$fp = fopen('parlaklik.json', 'w');
fwrite($fp, json_encode($response));
fclose($fp);

include 'parlaklik.html'; //sicaklik.html sayfasi cagriliyor

$url=$_SERVER['index_parlaklik.php']; 
header("Refresh: 10; URL=$url"); //sayfa 10 saniyede bir yenileniyor
?> 