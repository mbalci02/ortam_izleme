<?php
$servername = "localhost";
$username = "root";
$password = "*******";
$dbname = "Ortam_Izleme";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT ZAMAN,ZAMAN2,CO,LPG,DUMAN FROM Anlik_Olcumler ORDER BY ID DESC LIMIT 20";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
  //  echo "<table><tr><th>zaman2</th><th>SICAKLIK</th><th>NEM</th></tr>";
    // output data of each row
 $rows = array();

    while($row = $result->fetch_assoc()) {
    //    echo "<tr><td>" . $row["zaman2"]. "</td><td>" . $row["sicaklik"]. "</td><td> " . $row["nem"]. "</td></tr>";"<br />";
      //  $rows['date'] = $row["zaman2"];
        $rows[] = $row;
    }

$fp = fopen('gaz.json', 'w');
fwrite($fp, json_encode($rows));
fclose($fp);
//    echo "</table>";
} else {
    echo "0 results";
}
 //print json_encode($rows);

$conn->close();

include 'gaz.html'; //nem.html sayfasi cagriliyor

$url=$_SERVER['gaz.php']; 
header("Refresh: 5; URL=$url"); //sayfa 10 saniyede bir yenileniyor
?> 