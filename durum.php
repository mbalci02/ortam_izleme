<!DOCTYPE html>
<html>
<body>

<?php
echo 'ORTAMIN GENEL DURUMU'."<br>";
$servername = "localhost";
$username = "root";
$password = "********";
$dbname = "Ortam_Izleme";

// Veritabani baglantisi
$conn = new mysqli($servername, $username, $password, $dbname);
// Baglantinin kontrolu
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "SELECT ZAMAN, DURUM,SIVI_SEVIYE FROM Kayitli_Olcumler where ID>=3247 AND ID<=3257"; //ORDER BY ID DESC LIMIT 8";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // Sorgu sonuclarinin dizilere atanmasi
    while($row = $result->fetch_assoc()) {
	$sivi=$row["SIVI_SEVIYE"];
	if(($sivi)>3){
	echo "<br>". $row["ZAMAN"]. " --> ".$row["DURUM"]." SIVI SEVIYESI: ". $row["SIVI_SEVIYE"]. " CM"."<br>";}
	else{
	echo "<br>". $row["ZAMAN"]. " --> ". $row["DURUM"]. "<br>";}
    }
}else {
    echo "0 results";
}

$conn->close();

$url=$_SERVER['durum.php']; 
header("Refresh: 5; URL=$url"); //sayfa 10 saniyede bir yenileniyor
?> 

</body>
</html>