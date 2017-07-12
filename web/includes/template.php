<?
// this is the implementation of our template engine based for now on http://www.sitepoint.com/article/beyond-template-engine
   defined( "__OAKLEY_DB__" ) or die( "Direct Access to this location is not allowed." );

   class TemplateEngine
   {
   	     var $variables;
   	     var $templatePath;

   	     // constructor
   	     function TemplateEngine( $path = null )
   	     {
            $this->templatePath = $path;
   	     	$this->variables = array();
   	     }

   	     function set_path( $path )
   	     {
   	     	$this->templatePath = $path;
   	     }
   	     
   	     function add_variable( $name, $value )
   	     {
   	     	$this->variables[$name] = $value;
   	     }
   	     
   	     function add_multiple( $variables, $clear = false )
   	     {
   	     	if($clear)
   	     	{
   	     		$this->variables = $variables;
   	     	}
   	     	else
   	     	{
   	     		if( is_array( $variables ) )
   	     		{
   	     			$this->variables = array_merge( $this->variables, $variables );
   	     		}
   	     	}
   	     }
   	     
   	     function ApplyTemplate( $template )
   	     {
   	        extract( $this->variables );
            ob_start();
            include( $this->templatePath.$template );
            $renderedHTML = ob_get_contents( );
            ob_end_clean( );

            return $renderedHTML;
   	     }
   	     
   	     function ApplyTemplateDirect( $template )
   	     {
   	     	extract( $this->variables );
            ob_start();
            include( $this->templatePath.$template );
            ob_end_flush( );
   	     }
   }


?>
