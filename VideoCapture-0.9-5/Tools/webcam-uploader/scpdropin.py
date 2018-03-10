import os, tempfile


class ScpError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return `self.value`


havescp2 = havepscp = None

f, g = os.popen4('scp2.exe', 't')
if g.read()[:12] == 'SSH scp2.exe':
    havescp2 = 1
f.close()
g.close()

f, g = os.popen4('pscp.exe', 't')
if g.read()[:24] == 'PuTTY Secure Copy client':
    havepscp = 1
f.close()
g.close()

if not (havescp2 or havepscp):
    raise ScpError, 'found neither pscp.exe nor scp2.exe'


class FTP:
    def __init__(self, host, user, passwd):
        self.host = host
        self.user = user
        self.passwd = passwd

    def storbinary(self, command, fp, dummyport=None):
        remotefile = command[5:]  # my storbinary()-calls all start with 'STOR '
        tmpname = tempfile.mktemp()
        f = open(tmpname, 'wb')
        f.write(fp.read())
        f.close()
        arguments = tmpname + ' ' + self.user + '@' + self.host + ':' + remotefile
        if os.name == 'posix':
            if os.system('scp -Q ' + arguments):
                raise ScpError, 'scp return value is different from 0'
        else:  # 'nt'
            if havescp2:
                f, g = os.popen4('scp2.exe ' + arguments, 't')
                prompt = g.read(3)
                if prompt == 'You':  # are connecting to ... for the first time.
                    f.write('yes\n')
                    f.write(self.passwd + '\n')
                elif prompt == self.user[:3]:
                    f.write(self.passwd + '\n')
                else:
                    raise ScpError, 'unexpected prompt from scp2.exe'
                f.close()
                g.close()
            elif havepscp:
                f, g = os.popen4('pscp.exe -pw ' + self.passwd + ' ' + arguments, 't')
                f.close()
                g.close()
        os.remove(tmpname)

    storlines = storbinary

    def sendcmd(self, dummycmd):
        pass

    def close(self):
        pass
