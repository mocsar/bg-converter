import os
import converter

__author__ = 'mocsar'

import requests
import requests_ftp
import logging

requests_ftp.monkeypatch_session()
host = '192.168.25.182:3721'
s = requests.Session()

logger = logging.getLogger('tavla_main')

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

def process(file):
    logger.info('Processing: %s', file)
    resp = s.retr('ftp://{}/tavlaplus/{}'.format(host, file))
    if resp.status_code == 226:
        try:
            converter.convert(file, str(resp.content).replace('\r', '').splitlines())
            return True
        except Exception as ex:
            logger.error('Error while converting: %s', ex)
    else:
        text = ""
        try:
            text = resp.text
        except: pass
        logger.error('Response error: {}; {}'.format(resp.status_code, text))
    return False

def main():
    files = lst()
    processed = []
    oud_dir = 'converted'
    files = os.listdir(oud_dir)
    with open('processed_files.txt') as f:
        processed.extend(f.readlines())

    for file in files:
        if file not in processed:
            done = process(file)
            if done: processed.append(file)

    with open('processed_files.txt', 'w') as f:
        f.writelines(*processed)

if __name__ == "__main__":
    main()
