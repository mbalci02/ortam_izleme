<?php 
//http://stackoverflow.com/a/2467974
$servername = "localhost";
$username = "root";
$password = "******";
$dbname = "Ortam_Izleme";

// Create connection
$mysqli = new mysqli($servername, $username, $password, $dbname);

$query="SELECT ZAMAN2,NEM FROM Anlik_Olcumler"; 
$result=$mysqli->query($query)
	or die ($mysqli->error);

//store the entire response
//$response = array();

//the array that will hold the titles and links
$posts = array();
while($row=$result->fetch_assoc()) //mysql_fetch_array($sql)
{ 
$ZAMAN2=$row['ZAMAN2']; 
$NEM=$row['NEM']; 

//each item from the rows go in their respective vars and into the posts array
$posts[] = $NEM; 
$ZAMAN[]=$ZAMAN2*1000;
} 

echo json_encode($ZAMAN);

//creates the file

$p1=$ZAMAN[0];//1230764400001;
$p2=3600000;
$p3=sizeof($posts); //78907; // Burada veritabanaina baglanip, kayit sayisi almalisin.
$p4= array_values($posts);//array(1.2,2.3);
//array_push($p4,); 
$p4= implode(",", $p4);

$response = "{\"pointStart\":$p1,\"pointInterval\":$p2, \"dataLength\":$p3,\"data\":[$p4]}";
//creates the file
$fp = fopen('nem.json', 'w');
fwrite($fp, $response);
fclose($fp)

?> 