import os
import converter

__author__ = 'mocsar'

import requests
import requests_ftp
import logging

requests_ftp.monkeypatch_session()
host = '192.168.25.182:3721'
s = requests.Session()

logger = logging.getLogger('bg-main')


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


def process(tavla_file_name, gnu_file_name):
    logger.info('Processing: %s', tavla_file_name)
    resp = s.retr('ftp://{}/tavlaplus/{}'.format(host, tavla_file_name))
    if resp.status_code == 226:
        try:
            converter.convert(gnu_file_name, str(resp.content).replace('\r', '').splitlines())
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


def convert_to_gnu(tavla_file_name):
    name, ext = os.path.splitext(os.path.split(tavla_file_name)[1])
    return '{}-{}-{}--{}-{}-{}--{}.txt'.format(name[0:4], name[4:6], name[6:8], name[8:10], name[10:12], name[12:14], name[14:]), 'session' in name, ext


def main():
    oud_dir = 'converted'
    force_if_exists = True

    new_files = lst()
    old_files = os.listdir(oud_dir)
    for tavla_file_name in new_files:
        gnu_file_name, is_session, ext= convert_to_gnu(tavla_file_name)
        if (force_if_exists or gnu_file_name not in old_files) and (not is_session) and (ext == '.tp'):
            process(tavla_file_name, os.path.join(oud_dir, gnu_file_name))
        else: logger.info('skip to convert: {}'.format(tavla_file_name))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
