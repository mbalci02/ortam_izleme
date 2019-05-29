<html>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<?php
header('Content-Type: text/html; charset=utf-8');
$servername = "localhost";
$username = "root";
$password = "******";
$dbname = "Ortam_Izleme";

// Baglanti kurma
$conn = new mysqli($servername, $username, $password, $dbname);
// Baglanti kontrolu
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT ZAMAN,ZAMAN2,SICAKLIK,NEM,PARLAKLIK,SIVI_SEVIYE FROM Anlik_Olcumler ORDER BY ID DESC LIMIT 20";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
 
 $rows = array();

    while($row = $result->fetch_assoc()) {
          $rows[] = $row;
    }
$fp = fopen('olcumler.json', 'w');
fwrite($fp, json_encode($rows));
fclose($fp);

} else {
    echo "0 results";
}


$conn->close();

include 'sicaklik.html'; //sicaklik.html sayfasi cagriliyor

$url=$_SERVER['olcumler.php']; 
header("Refresh: 10; URL=$url"); //sayfa 10 saniyede bir yenileniyor*/
?> 
</html>