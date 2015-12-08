from reader import Reader

__author__ = 'mocsar'

import requests
import requests_ftp
import logging

logger = logging.getLogger('bg.ftpreader')

class FTPReader(Reader):
    def __init__(self, host):
        requests_ftp.monkeypatch_session()
        self.s = requests.Session()
        self.host = host

    def list_files(self):
        resp = self.s.nlst('ftp://{}/tavlaplus/'.format(self.host))
        if resp.status_code == 226:
            return str(resp.content).replace('\r', '').splitlines()
        else:
            text = ""
            try:
                text = resp.text
            except: pass
            raise Exception('Response error: {}; {}'.format(resp.status_code, text))


    def read_lines(self, file_name):
        logger.info('Processing: %s', file_name)
        resp = self.s.retr('ftp://{}/tavlaplus/{}'.format(self.host, file_name))
        if resp.status_code == 226:
            try:
                return str(resp.content).replace('\r', '').splitlines()
            except Exception as ex:
                logger.error('Error while converting: %s', ex)
        else:
            text = ""
            try:
                text = resp.text
            except: pass
            logger.error('Response error: {}; {}'.format(resp.status_code, text))
        return None
