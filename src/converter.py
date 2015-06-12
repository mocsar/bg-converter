import json
import logging

__author__ = 'mocsar'

logger = logging.getLogger('bg-converter')


def _handle_line(converted, in_line):
    """
    :type in_line: str
    """
    time, thread, msg = in_line.split(' - ', 3)
    if msg.startswith('RES : '):
        msg = msg[6:]
        j = json.loads(msg)
        converted.append(json.dumps(j, sort_keys=True) + '\n')


def convert(gfile, content):
    # logger.debug('content: {}'.format(content))
    converted = []
    for in_line in content:
        _handle_line(converted, in_line)
    logger.debug('writing converted content to : {}'.format(gfile))
    with open(gfile, 'w') as out:
        out.writelines(converted)
    pass