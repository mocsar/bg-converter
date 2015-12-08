import logging
from reader import Reader
from os import listdir
from os.path import isfile, join

__author__ = 'mocsar'

logger = logging.getLogger('bg.localreader')

class LocalReader(Reader):
    def __init__(self, folder):
        self.folder = folder

    def list_files(self):
        return [ f for f in listdir(self.folder) if isfile(join(self.folder,f)) ]

    def read_lines(self, file_name):
        file = join(self.folder, file_name)
        logger.debug('file: %s' % file)
        with open(file) as f:
            return f.readlines()

