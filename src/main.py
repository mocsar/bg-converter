#!/usr/bin/env python

import os
os.chdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
import converter
from ftpreader import FTPReader
from localreader import LocalReader

__author__ = 'mocsar'

import logging

logger = logging.getLogger('bg.main')

def convert_to_gnu(tavla_file_name):
    name, ext = os.path.splitext(os.path.split(tavla_file_name)[1])
    return '{}-{}-{}--{}-{}-{}--{}.txt'.format(name[0:4], name[4:6], name[6:8], name[8:10], name[10:12], name[12:14], name[14:]), 'session' in name, ext


def main():
    oud_dir = 'converted'
    force_if_exists = True

    reader = FTPReader('192.168.25.182:3721')
    # reader = LocalReader('C:\\Users\\mocsar\\projects\\bg-py\\bg-converter\\gnu_files\\tavlaplus2')

    new_files = reader.list_files()
    old_files = os.listdir(oud_dir)
    for tavla_file_name in new_files:
        gnu_file_name, is_session, ext= convert_to_gnu(tavla_file_name)
        gnu_file_name = os.path.join(oud_dir, gnu_file_name)
        if (force_if_exists or gnu_file_name not in old_files) and (not is_session) and (ext == '.tp'):
            logger.info('Processing: %s', tavla_file_name)
            lines = reader.read_lines(tavla_file_name)
            try:
                converted = converter.Converter().convert(lines)
                logger.debug('writing converted content to : {}'.format(gnu_file_name))
                with open(gnu_file_name, 'w') as out:
                    n__join = u'\n'.join(converted)
                    out.write(n__join.encode('utf-8'))
            except Exception as ex:
                logger.exception('Error while converting: %s', ex)
        else: logger.info('skip to convert: {}'.format(tavla_file_name))


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
