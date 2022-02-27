<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
header("refresh: 300;");
$myDate = date('Y-m-d');
$chart = "Combo-$myDate.png";

$db = new SQLite3('/home/pi/BirdNET-Pi/scripts/birds.db', SQLITE3_OPEN_CREATE | SQLITE3_OPEN_READWRITE);
if($db == False) {
  echo "Database is busy";
  header("refresh: 0;");
}

$statement = $db->prepare('SELECT COUNT(*) FROM detections');
if($statement == False) {
  echo "Database is busy";
  header("refresh: 0;");
}
$result = $statement->execute();
$totalcount = $result->fetchArray(SQLITE3_ASSOC);

$statement2 = $db->prepare('SELECT COUNT(*) FROM detections WHERE Date == DATE(\'now\', \'localtime\')');
if($statement2 == False) {
  echo "Database is busy";
  header("refresh: 0;");
}
$result2 = $statement2->execute();
$todaycount = $result2->fetchArray(SQLITE3_ASSOC);

$statement3 = $db->prepare('SELECT COUNT(*) FROM detections WHERE Date == Date(\'now\', \'localtime\') AND TIME >= TIME(\'now\', \'localtime\', \'-1 hour\')');
if($statement3 == False) {
  echo "Database is busy";
  header("refresh: 0;");
}
$result3 = $statement3->execute();
$hourcount = $result3->fetchArray(SQLITE3_ASSOC);

$statement4 = $db->prepare('SELECT Com_Name, Sci_Name, Date, Time, Confidence, File_Name FROM detections ORDER BY Date DESC, Time DESC LIMIT 1');
if($statement4 == False) {
  echo "Database is busy";
  header("refresh: 0;");
}
$result4 = $statement4->execute();
$mostrecent = $result4->fetchArray(SQLITE3_ASSOC);
$comname = preg_replace('/ /', '_', $mostrecent['Com_Name']);
$sciname = preg_replace('/ /', '_', $mostrecent['Sci_Name']);
$comname = preg_replace('/\'/', '', $comname);
$filename = "/By_Date/".$mostrecent['Date']."/".$comname."/".$mostrecent['File_Name'];

$statement5 = $db->prepare('SELECT COUNT(DISTINCT(Com_Name)) FROM detections WHERE Date == Date(\'now\',\'localtime\')');
if($statement5 == False) {
  echo "Database is busy";
  header("refresh: 0;");
}
$result5 = $statement5->execute();
$speciestally = $result5->fetchArray(SQLITE3_ASSOC);
?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Overview</title>
<style>
</style>
</head>
<body>
 <div>
  </div>
    <table>
      <tr>
        <th>Total</th>
        <th>Today</th>
        <th>Last Hour</th>
        <th>Species Detected Today</th>
      </tr>
      <tr>
        <td><?php echo $totalcount['COUNT(*)'];?></td>
        <form action="" method="POST">
        <td><input type="hidden" name="view" value="Recordings"><button type="submit" name="date" value="<?php echo date('Y-m-d');?>"><?php echo $todaycount['COUNT(*)'];?></button></td>
        </form>
        <td><?php echo $hourcount['COUNT(*)'];?></td>
        <form action="" method="POST">
        <td><button type="submit" name="view" value="Species Stats"><?php echo $speciestally['COUNT(DISTINCT(Com_Name))'];?></button></td>
        </form>
      </tr>
    </table>
</div>
 <div>

    <table>
      <tr>
        <th>Most Recent Detection</th>
        <th>Scientific Name</th>
        <th>Common Name</th>
        <th>Listen</th>
        <th>Confidence</th>
      </tr>
      <tr>
        <td><?php echo $mostrecent['Date']."<br>".$mostrecent['Time'];?></td>
        <td><a href="https://wikipedia.org/wiki/<?php echo $sciname;?>" target="_blank"/><?php echo $mostrecent['Sci_Name'];?></a></td>
        <form action="" method="POST">
          <td>
            <input type="hidden" name="view" value="Species Stats">
            <button type="submit" name="species" value="<?php echo $mostrecent['Com_Name'];?>"><?php echo $mostrecent['Com_Name'];?></button>
          </td>
        </form>
        <td class="spectrogram" ><video controls poster="<?php echo $filename.".png";?>"><source src="<?php echo $filename;?>"></video></td>
        <td><?php echo $mostrecent['Confidence'];?></td>
      </tr>
    </table>
  </div>
<?php
if (file_exists('/home/pi/BirdSongs/Extracted/Charts/'.$chart)) {
  echo "<img class=\"centered\" src=\"/Charts/$chart?nocache=time()\">";
} else {
  echo "<p>No Detections For Today</p>";
}
?>
    <h3>Currently Analyzing</h3>
<img class="centered" style="width:100%;" src='/spectrogram.png?nocache=<?php echo time();?>' >
</html>
