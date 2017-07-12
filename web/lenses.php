<?php

$db_user = 'aquariaz_oakley';
$db_password = 'Lx3SFJg978hB1cE1';
$db_host = 'aquaria.za.net';
$db_databasename = 'aquariaz_oakleydb';

$dsn = 'mysql:host='.$db_host.';dbname='.$db_databasename;
// Connect to the database, run a query, handle errors
$pdo = new PDO($dsn, $db_user, $db_password);

$statement = $pdo->query("SELECT name FROM lenstype");

if ($statement === false)
{
    throw new Exception('There was a problem running this query');
}

?>

<!DOCTYPE html>
<html>
    <head>
        <title>Oakley DB - Lenses</title>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    </head>
    <body>
        <h2>Oakley DB - Lenses</h2>
        [<a href="index.php">Sunglasses</a>] [<a href="lenses.php">Lenses</a>]
        <br />
        <ul>
<?php while ($row = $statement->fetch(PDO::FETCH_ASSOC)):
            echo '<li>'.htmlentities($row['name']).'<ul>';
$s2 = $pdo->prepare("SELECT l.id, l.name FROM lens l JOIN lenstype lt on l.lenstypeid = lt.id WHERE lt.name=?");
if ($s2 === false)
{
    throw new Exception('There was a problem running this query');
}

$result = $s2->execute(array( $row['name'], ) );

if ($result === false)
{
    throw new Exception('There was a problem running this query');
}

while ($r2 = $s2->fetch(PDO::FETCH_ASSOC)):
      echo '<li><a href="lensdetails.php?id='.htmlentities($r2['id']).'">'.htmlentities($r2['name']).'</a></li>';
endwhile;
            echo '</ul></li>';
endwhile ?>
        </ul>
   </body>
</html>
