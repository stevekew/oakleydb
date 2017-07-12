<?php
defined( "__OAKLEY_DB__" ) or die( "Direct Access to this location is not allowed." );
     // Logging class
class Logger
{
      var $filehandle;
      var $filename;
      var $dateFormat;

      function Logger( $filename, $path = "./" )
      {
            $this->filename = $path.$filename;
            $this->dateFormat = "[d-m-Y H:i] ";

            $this->OpenLogFile( );
      }

      function OpenLogFile( )
      {
            $this->filehandle = fopen ($this->filename, "a") or die("Could not open log file.");
            $this->LogInfo( "*** Logging Started ***" );
      }

      function CloseLogFile( )
      {
      	    $this->LogInfo( "*** Logging Stopped ***" );
      	    fclose( $this->filehandle );
      }
      
      function SetDateFormat( $dateFormat )
      {
      	    $this->dateFormat = $dateFormat;
      }
      
      function WriteToLog( $string )
      {
      	    $date = date( $this->dateFormat );
            fwrite( $this->filehandle, $date.$string."\n" );
      }
      
      function LogError( $error )
      {
            $this->WriteToLog( "ERROR: ".$error );
      }

      function LogWarning( $warning )
      {
            $this->WriteToLog( "WARNING: ".$warning );
      }

      function LogInfo( $information )
      {
            $this->WriteToLog( $information );
      }
}
?>
