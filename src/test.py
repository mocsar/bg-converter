
__author__ = 'mocsar'

# import urllib
# import shutil
# import urllib2
# from contextlib import closing
import requests
import requests_ftp


# a, b = urllib.urlretrieve('ftp://192.168.25.182:3721/tavlaplus/20150602063318-621_session.tp')

# a, b = urllib.urlretrieve('ftp://192.168.25.182:3721/tavlaplus/', 'dir')
# print 'a', a
# print 'b.fp', b.fp.getvalue()
#
#
#
# with closing(urllib2.urlopen('ftp://192.168.25.182:3721/tavlaplus/20150602063318-621_session.tp')) as r:
#     with open('file', 'wb') as f:
#         shutil.copyfileobj(r, f)

requests_ftp.monkeypatch_session()
host = '192.168.25.182:3721'
s = requests.Session()

def lst():
    resp = s.nlst('ftp://{}/tavlaplus/'.format(host))
    if resp.status_code == 226:
        return str(resp.content).replace('\r', '').splitlines()
    else:
        text = ""
        try:
            text = resp.text
        except: pass
        raise Exception('Response error: {}; {}'.format(resp.status_code, text))

def get(file):
    resp = s.retr('ftp://{}/tavlaplus/{}'.format(host, file))
    if resp.status_code == 226:
        return str(resp.content).replace('\r', '').splitlines()
    else:
        text = ""
        try:
            text = resp.text
        except: pass
        raise Exception('Response error: {}; {}'.format(resp.status_code, text))

def main():
    files = lst()
    for file in files:
        print get(file)

if __name__ == "__main__":
    main()
