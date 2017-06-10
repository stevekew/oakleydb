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
    $lensId = $_GET['id'];
}
else
{
    // So we always have a post ID var defined
    $lensId = 0;
}

if (!is_numeric($lensId))
{
    $lensId = 0;
}


$statement = $pdo->prepare("SELECT * FROM lens WHERE id = :id");

if ($statement === false)
{
    throw new Exception('There was a problem running this query');
}

$result = $statement->execute(array('id' => $lensId, ) );

if ($result === false)
{
    throw new Exception('There was a problem running this query');
}

$row = $statement->fetch(PDO::FETCH_ASSOC);

?>

<!DOCTYPE html>
<html>
    <head>
        <title>Oakley DB</title>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    </head>
    <body>
        <h2>Oakley DB - <?php echo htmlentities($row['name']); ?></h2>
        <br />
       <table>
<?php
            echo '<tr><td>Lens</td><td>'.htmlentities($row['name']).'</td> </tr>';
            echo '<tr><td>Base</td><td>'.htmlentities($row['base']).'</td> </tr>';
            echo '<tr><td>Coating</td><td>'.htmlentities($row['coating']).'</td> </tr>';
            echo '<tr><td>Transmission</td><td>'.htmlentities($row['transmission']).'</td> </tr>';
            echo '<tr><td>Index</td><td>'.htmlentities($row['transindex']).'</td> </tr>';
	    echo '<tr><td>Purpose</td><td>'.htmlentities($row['purpose']).'</td> </tr>';
	    echo '<tr><td>Lighting</td><td>'.htmlentities($row['lighting']).'</td> </tr>';
?>
        </table>
   </body>
</html>
