<?php

$db_user = '';
$db_password = '';
$db_host = '';
$db_databasename = '';

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
        <h2>Oakley DB</h2>
        <ul>
<?php while ($row = $statement->fetch(PDO::FETCH_ASSOC)):
            echo '<li><a href="details.php?id='.htmlentities($row['id']).'">'.htmlentities($row['name']).'</a> ['.htmlentities($row['sku']).']</li>';
endwhile ?>
        </ul>
   </body>
</html>
