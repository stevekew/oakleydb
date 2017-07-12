<?php
// this file contains useful functions
//   require_once("../config.php"); // this is the main configuration file
defined( "__OAKLEY_DB__" ) or die( "Direct Access to this location is not allowed." );

function GenerateHTMLHeaders()
{
    return "<html>\n";
}

function GeneratePageHeaders()
{
    return "<head>\n<title>This is the title</title>\n</head>\n";
}

function GeneratePageFooters()
{

}

function GenerateHTMLFooters()
{
    return "</html>";
}

function GenerateMenu( $params = array() )
{
    global $contentDir, $menuSep, $mainPage, $templatesPath;
    $dir = "./".$contentDir;
    $dirName = "";

    $menuitems = array();
    $item = array( "title" => "",
                   "link" => "",
                   "active" => false );


    if( empty( $params ) )
    {
    	// can work out here what the current menu item is use it for the class active menu
//    	echo( "Empty");
    }

    // we want to parse the main content directory structure and
    if ($handle = opendir( $dir ))
    {
       /* This is the correct way to loop over the directory. */
       while (false !== ($file = readdir($handle)))
       {
       	    if( is_dir( $dir."/".$file ) )
       	    {
                if( ( $file != "." ) and ( $file != ".." ) )
                {
                	// ok, parse the directory name here and pull out the prefix
                	$dirName = strstr( $file, $menuSep );
                	$dirName = trim( $dirName, $menuSep );

                    $filename = $dir."/".$file."/link.txt";
                	// need to check if it is just a link or an actual content folder
                	if( file_exists( $filename ) )
                	{
                		// yes, so open the link file and use it
                		$filehandle = fopen ($filename, "r") or die("Could not open file");
                		
                		while (!feof($filehandle))
                        {
                        	// get the link
                            $data = fgets($filehandle);
                        }
                        
                        fclose ($filehandle);

                        $item['title'] = str_replace( "_", " ", $dirName );
                        $item['link'] = $data;
                        
                        $menuitems[] = $item;
                	}
                    else
                    {
                    	$item['title'] = str_replace( "_", " ", $dirName );
                        $item['link'] = $mainPage."?link=".$file;
                        
                        $menuitems[] = $item;
                    }
                }
            }
       }

       closedir($handle);
    }


    // create am instance of the template engine
    $template = & new TemplateEngine( $templatesPath );
    
    // set the variables for the template
    $template->add_variable( "menu_items", $menuitems );

    // load the template and get the html
    $menuHTML = $template->ApplyTemplate( "menu.template.php" );

    return $menuHTML;
}

function GenerateContent( $params  = array() )
{
    // this function will call out to the correct script based on the content
    global $defaultContent;

    $content = $defaultContent; // start by setting it to default

    if( !empty( $params ) )
    {
    	// parameters are not empty, so lets see what we are doing
    	if( array_key_exists("module", $params ) )
    	{
    		// have the module to execute, so put it in the content
    		$content = $params['module'];
    	}

    }

    if( file_exists( "./scripts/".$content.".php" ) )
    {
        // want to call out to the module, so include the script and call it
        require_once( "./scripts/".$content.".php" ); // this is the main configuration file
        
        /* // old method used to call procedure based scripts
        if( function_exists( $content ) )
        {
        	return $content( $params );
        }   */

        $scriptClass = $content."_script";
        $class = new $scriptClass( );
        return $class->execute( $params );
    }
}

// will format the date using the defined formatter
function Format_Date( $timestamp, $mode = "default" )
{
    global $defaultDateFormatter;
    
    $formatter = $defaultDateFormatter;
    
    $var = "";

    if( $mode != "default" )
    {
        $var = $GLOBALS[$mode."DateFormatter"];

    	if( isset( $var ) )
    	{
            $formatter = $var;
        }
    }
    
    return date( $formatter, $timestamp );
}

?>
