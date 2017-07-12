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

$statement = $pdo->prepare("SELECT m.*, l.name as lens, s.name as style FROM model m JOIN lens l on m.lensid = l.id JOIN style s on m.styleid = s.id WHERE m.id = :id");

if ($statement === false)
{
    throw new Exception('There was a problem running this query');
}

$result = $statement->execute(array('id' => $modelId, ) );

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
        <h2>Oakley DB - <?php echo htmlentities($row['style']).': '.htmlentities($row['name']); ?></h2>
        <br />
       <table>
<?php
            echo '<tr><td>Style</td><td>'.htmlentities($row['style']).'</td> </tr>';
            echo '<tr><td>Model</td><td>'.htmlentities($row['name']).'</td> </tr>';
            echo '<tr><td>Frame</td><td>'.htmlentities($row['framecolour']).'</td> </tr>';
            echo '<tr><td>Lens</td><td><a href="lensdetails.php?id='.htmlentities($row['lensid']).'">'.htmlentities($row['lens']).'</a></td> </tr>';
            echo '<tr><td>SKU</td><td>'.htmlentities($row['sku']).'</td> </tr>';
            echo '<tr><td>List Price</td><td>'.htmlentities($row['listprice']).'</td> </tr>';
            echo '<tr><td>Release Date</td><td>'.htmlentities($row['releasedate']).'</td> </tr>';
            echo '<tr><td>Retire Date</td><td>'.htmlentities($row['retiredate']).'</td> </tr>';
           
            if(!empty($row['basecurve']))
            {
                echo '<tr><td>Lens Base Curve</td><td>'.htmlentities($row['basecurve']).'</td> </tr>';
            }

            if(!empty($row['note']))
            {
                echo '<tr><td>Note</td><td>'.htmlentities($row['note']).'</td> </tr>';
            }

            if(!empty($row['signature']))
            {   
                echo '<tr><td>Signature</td><td>'.htmlentities($row['signature']).'</td> </tr>';
            }

            if(!empty($row['exclusive']))
            {   
                echo '<tr><td>Exclusive</td><td>'.htmlentities($row['exclusive']).'</td> </tr>';
            }

	    echo '</table>';

            if (($row['image'] != NULL) && (strlen($row['image']) > 0))
            {
                   echo '<img src="'.str_replace("o-review.com", "aquaria.za.net/oakleydb", htmlentities($row['image'])).'" />';        
            } 
?>
   </body>
</html>
