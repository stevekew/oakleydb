<?php

$db_user = 'aquariaz_oakley';
$db_password = 'Lx3SFJg978hB1cE1';
$db_host = 'aquaria.za.net';
$db_databasename = 'aquariaz_oakleydb';

$dsn = 'mysql:host='.$db_host.';dbname='.$db_databasename;
// Connect to the database, run a query, handle errors
$pdo = new PDO($dsn, $db_user, $db_password);

// Get the post ID
if (isset($_GET['id']))
{
    $styleId = $_GET['id'];
}
else
{
    // So we always have a post ID var defined
    $styleId = 0;
}

if (!is_numeric($styleId))
{
    $styleId = 0;
}

$s1 = $pdo->prepare("SELECT name FROM style WHERE id = :id");

if ($s1 === false)
{
    throw new Exception('There was a problem running this query');
}
$res1 = $s1->execute(array('id' => $styleId, ) );

if ($res1 === false)
{
    throw new Exception('There was a problem running this query');
}

$row1 = $s1->fetch(PDO::FETCH_ASSOC);

$statement = $pdo->prepare("SELECT * FROM model WHERE styleid = :id");

if ($statement === false)
{
    throw new Exception('There was a problem running this query');
}

$result = $statement->execute(array('id' => $styleId, ) );

if ($result === false)
{
    throw new Exception('There was a problem running this query');
}

?>

<!DOCTYPE html>
<html>
    <head>
        <title>Oakley DB</title>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    </head>
    <body>
        <h2>Oakley DB - <?php echo htmlentities($row1['name']) ?></h2>
        <ul>
<?php while ($row = $statement->fetch(PDO::FETCH_ASSOC)):
            echo '<li><img src="'.str_replace("o-review.com", "aquaria.za.net/oakleydb", htmlentities($row['imagesmall'])).'" />&nbsp;&nbsp;<a href="details.php?id='.htmlentities($row['id']).'">'.htmlentities($row['name']).'</a> ['.htmlentities($row['sku']).']</li>';
endwhile ?>
        </ul>
   </body>
</html>
