<?php


function g
<html>
    <head>
        <title>Oakley DB</title>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    </head>
    <body>
        <h2>Oakley DB</h2>
        [<a href="index.php">Sunglasses</a>] [<a href="lenses.php">Lenses</a>] <form method="post" action="search.php"><label>Search:</label><input type="text" id="query" name="query"/><input type="submit" name = 'search' value="Search" /> </form>
        <br />
        <ul>
<?php while ($row = $statement->fetch(PDO::FETCH_ASSOC)): ?>
        <li><?php
            echo  htmlentities($row['name']);
            $s2 = $pdo->query('SELECT s.* FROM style s JOIN familystylemap m on m.styleid = s.id JOIN family f on m.familyid = f.id WHERE m.familyid='.$row['id'].' ORDER by s.name asc');
            if ($s2 === false)
            {
                throw new Exception('Error querying for styles');
            }
            ?><ul><?php
            while ($r2 = $s2->fetch(PDO::FETCH_ASSOC)):

              $s3 = $pdo->query('SELECT COUNT(*) as count FROM model WHERE styleid='.$r2['id']);
              if($s3 === false)
              {
                  throw new Exception('Error querying for model count');
              }
              $count_row = $s3->fetch(PDO::FETCH_ASSOC);
              echo '<li><a href="models.php?id='.htmlentities($r2['id']).'">'.htmlentities($r2['name']).'</a> ('.htmlentities($count_row['count']).')</li>';
            endwhile
            ?></ul><?php
      ?></li>

<?php endwhile ?>
        </ul>
   </body>
</html>



?>
