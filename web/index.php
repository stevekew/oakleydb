<?php

$db_user = '';
$db_password = '';
$db_host = '';
$db_databasename = '';

$dsn = 'mysql:host='.$db_host.';dbname='.$db_databasename;
// Connect to the database, run a query, handle errors
$pdo = new PDO($dsn, $db_user, $db_password);

$statement = $pdo->query("SELECT * FROM family");

if ($statement === false)
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
<?php while ($row = $statement->fetch(PDO::FETCH_ASSOC)): ?>
        <li><?php
            echo  htmlentities($row['name']);
            $s2 = $pdo->query('SELECT * FROM style WHERE familyid='.$row['id']);
            if ($s2 === false)
            {
                throw new Exception('Error querying for styles');
            }
            ?><ul><?php
            while ($r2 = $s2->fetch(PDO::FETCH_ASSOC)):
              echo '<li><a href="models.php?id='.htmlentities($r2['id']).'">'.htmlentities($r2['name']).'</a></li>';
            endwhile
            ?></ul><?php
      ?></li>

<?php endwhile ?>
        </ul>
   </body>
</html>
