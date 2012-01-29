#!/usr/bin/env python
shell = open("lsdshell.py","r").read().encode("base64")
x = open("installertemplate.php", "r").read().replace("REPLACE ME WITH BASE64 ENCODED LSDSHELL",shell)
installer = open("installer.php","w")
installer.write(x)
