<?php
$servername = "localhost";
$username = "root";
$password = "******";
$dbname = "Ortam_Izleme";

$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
    }

$query="SELECT ZAMAN2,SICAKLIK, NEM,CO,LPG FROM Anlik_Olcumler ORDER BY ID DESC LIMIT 20;

$result=$mysqli->query($query)
	or die ($mysqli->error);

//store the entire response
$response=array();

//the array that will hol the titles and links
$posts=array();

while ($rows=$result->fetch_assoc()) //mysql_fetch_array($sql)
{
$ZAMAN2=$row['ZAMAN2'];
$SICAKLIK=$row['SICAKLIK'];

//each item from the rows go in their respective vars and into the posts array
$posts[]=array('ZAMAN2'=>$ZAMAN2, 'SICAKLIK'=>$SICAKLIK);
}

//the posts array goes into the response
$response['posts']=$posts;

//create the file
$fp=fopen('results.json','w');
fwrite($fp, json_encode($response));
print json_encode($response);
fclose($fp);
?>
