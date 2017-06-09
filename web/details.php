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
    $modelId = $_GET['id'];
}
else
{
    // So we always have a post ID var defined
    $modelId = 0;
}

if (!is_numeric($modelId))
{
    $modelId = 0;
}


$statement = $pdo->prepare("SELECT * FROM model WHERE id = :id");

if ($statement === false)
{
    throw new Exception('There was a problem running this query');
}

$result = $statement->execute(array('id' => $modelId, ) );

if ($result === false)
{
    throw new Exception('There was a problem running this query');
}

$row = $statement->fetch(PDO::FETCH_ASSOC));

?>

<!DOCTYPE html>
<html>
    <head>
        <title>Oakley DB</title>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    </head>
    <body>
        <h2>Oakley DB - <?php echo htmlentities($row['name']) ?></h2>
        <br />

        <table>
<?php
            echo '<tr><td>Model</td><td>'.htmlentities($row['name']).'</td> </tr>\n'
            echo '<tr><td>Frame Colour</td><td>'.htmlentities($row['frame']).'</td> </tr>\n'
            echo '<tr><td>Lens</td><td>'.htmlentities($row['lens']).'</td> </tr>\n'
            echo '<tr><td>SKU</td><td>'.htmlentities($row['sku']).'</td> </tr>\n'
            echo '<tr><td>List Price</td><td>'.htmlentities($row['listprice']).'</td> </tr>\n'
?>
        </table>
   </body>
</html>