# coding=utf-8
import json
import logging

__author__ = 'mocsar'

logger = logging.getLogger('bg.converter')

class Converter(object):

    def __init__(self):
        self.state = None
        self.turn_counter = 1
        self.game_counter = 1
        self.active_player = None
        self.my_id = None
        self.other_name = None
        self.other_id = None

        self.dice = {}
        self.move = {}

    def game_over(self, j):
        self.turn_counter = 1
        self.active_player = None
        self.dice = {}
        self.move = {}

        players = j.get('players', None)
        winner = None
        if players:
            for p in players:
                if p.get('isWinner', None): winner = p.get('userId', None)

    def format_move(self, id, inverse=False):
        move = ''
        if self.move.get(id, None):
            for m in self.move.get(id):
                if inverse:
                    move += '{}/{} '.format(max(0, 24 - m['f']), max(0, 24 - m['t']))
                else:
                    move += '{}/{} '.format(max(0, m['f'] + 1), max(0, m['t'] + 1))
        move.strip()
        return move

    def handle_event(self, converted, resreq, j):
            """
            :type j: dict[str, str]
            :type converted: []
            :type resreq: basestring
            """
            if "CLIENT_USER_INFO_CHANGE" == j.get('commandName', None):
                if u"Mocsár Kálmán" == j.get('name', None):
                    self.my_id = j.get('userId', None)
                else:
                    self.other_name = j.get('name', None)
                    self.other_id = j.get('userId', None)
                return

            if self.state is None:
                if "CLIENT_GAME_START" == j.get('commandName', None):
                    self.active_player = j.get('turn', None)
                    self.state = 'WAIT_FOR_ROLL'
                    converted.append('')
                    converted.append(' Game {}'.format(self.game_counter))
                    self.game_counter += 1
                    converted.append(u' {:<33} {}'.format(u'{} : {}'.format(self.other_name[:20], 0), '{} : {}'.format('mocsar', 0)))
                if "CLIENT_GAME_OVER" == j.get('commandName', None):
                    self.game_over(j)
                    self.state = None

            elif self.state == 'WAIT_FOR_ROLL':
                if "SERVER_GAME_ROLL_DICE" == j.get('commandName', None):
                    self.dice[self.active_player] = j.get('dice', None)
                    self.state = 'WAIT_FOR_MOVE'
                if "CLIENT_GAME_OVER" == j.get('commandName', None):
                    self.game_over(j)
                    self.state = None

            elif self.state == 'WAIT_FOR_MOVE':
                if "SERVER_GAME_TURN_PLAY" == j.get('commandName', None) and j.get('turn', None):
                    self.move[self.active_player] = j.get('move', None)
                    if self.active_player == self.my_id :
                        line = '{:>3})'.format(self.turn_counter)
                        self.turn_counter += 1
                        if self.dice.get(self.other_id, None):
                            move = self.format_move(self.other_id, inverse=True)
                            line += ' {}{}: {:<27}'.format(self.dice.get(self.other_id)[0], self.dice.get(self.other_id)[1], move)
                        else:
                            line += '                                '
                        move = self.format_move(self.my_id)
                        line += '{}{}: {:<27}'.format(self.dice.get(self.my_id)[0], self.dice.get(self.my_id)[1], move)
                        converted.append(line)
                        self.dice = {}
                        self.move = {}
                    self.active_player = j.get('turn', None)
                    self.state = 'WAIT_FOR_ROLL'
                if "CLIENT_GAME_OVER" == j.get('commandName', None):
                    self.game_over(j)
                    self.state = None


    def handle_line(self, converted, in_line):
        """
        :type in_line: str
        """
        try:
            time, thread, msg = in_line.split(' - ', 3)
        except Exception as ex:
            logger.error('could not split: %s   %s', in_line, ex)
            return
        if msg.startswith('RES : ') or msg.startswith('REQ : '):
            resreq = msg[:3]
            msg = msg[6:]
            # logger.debug('json %s' % msg)
            try:
                j = json.loads(msg)
            except Exception as ex:
                logger.error('could not decode json %s', msg)
                return
            if j is not None: self.handle_event(converted, resreq, j)


    def convert(self, content):
        # logger.debug('content: {}'.format(content))
        converted = [' 64 point match']
        for in_line in content:
            self.handle_line(converted, in_line)
        return converted