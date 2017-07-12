<?php

$db_user = 'aquariaz_oakley';
$db_password = 'Lx3SFJg978hB1cE1';
$db_host = 'aquaria.za.net';
$db_databasename = 'aquariaz_oakleydb';

$dsn = 'mysql:host='.$db_host.';dbname='.$db_databasename;
// Connect to the database, run a query, handle errors
$pdo = new PDO($dsn, $db_user, $db_password);

// Get the post ID
if(isset($_POST['search'])) {
    if( isset( $_POST['query']) ) {
        $query = $_POST['query'];
    }
}

$statement = $pdo->prepare("SELECT m.*, s.name as style FROM model m JOIN style s on m.styleid = s.id WHERE m.sku like ? OR m.name like ? OR s.name like ?");

if ($statement === false)
{
    throw new Exception('There was a problem running this query');
}

$query_str = '%'.$query.'%';

$result = $statement->execute(array($query_str, $query_str, $query_str) );

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
            echo '<li><a href="details.php?id='.htmlentities($row['id']).'">'.htmlentities($row['style']).': '.htmlentities($row['name']).'</a> ['.htmlentities($row['sku']).']</li>';
endwhile ?>
        </ul>
   </body>
</html>


