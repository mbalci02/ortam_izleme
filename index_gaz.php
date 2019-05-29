<?php 
//http://stackoverflow.com/a/2467974
$servername = "localhost";
$username = "root";
$password = "*******";
$dbname = "Ortam_Izleme";

// Create connection
$mysqli = new mysqli($servername, $username, $password, $dbname);

$query="SELECT ZAMAN2,CO,LPG,DUMAN FROM Kayitli_Olcumler"; 
$result=$mysqli->query($query)
	or die ($mysqli->error);

//store the entire response
$response = array();

//the array that will hold the titles and links
$posts = array();
while($row=$result->fetch_assoc()) //mysql_fetch_array($sql)
{ 
$ZAMAN2=$row['ZAMAN2']; 
$CO=$row['CO']; 
$LPG=$row['LPG']; 
$DUMAN=$row['DUMAN']; 


//each item from the rows go in their respective vars and into the posts array
$co[] = array($ZAMAN2*1000,$CO*1); 
$lpg[] = array($ZAMAN2*1000,$LPG*1); 
$duman[] = array($ZAMAN2*1000,$DUMAN*1); 
} 

////The CO array goes into the response
$response1 = $co;
//echo "<h1>" . $co . "</h1>";
//creates the file
$fp1 = fopen('co.json', 'w');
fwrite($fp1, json_encode($response1));
fclose($fp1);

////The LPG array goes into the response
$response2 = $lpg;
//echo "<h1>" . $lpg . "</h1>";
//creates the file
$fp2 = fopen('lpg.json', 'w');
fwrite($fp2, json_encode($response2));
fclose($fp2);

////The DUMAN array goes into the response
$response3 = $duman;
//echo "<h1>" . $duman . "</h1>";
//creates the file
$fp3 = fopen('duman.json', 'w');
fwrite($fp3, json_encode($response3));
fclose($fp3);

include 'gaz.html'; //sicaklik.html sayfasi cagriliyor

$url=$_SERVER['index_gaz.php']; 
header("Refresh: 30; URL=$url"); //sayfa 30 saniyede bir yenileniyor
?> 