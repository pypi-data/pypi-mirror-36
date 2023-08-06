#!/usr/bin/env python
"""beanstalkc3 - A beanstalkd Client Library for Python"""

import os
import logging
import socket
import sys


__license__ = '''
Copyright (C) 2008-2016 Andreas Bolka

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

__version__ = '0.1.0'


DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 11300
DEFAULT_PRIORITY = 2 ** 31
DEFAULT_TTR = 120
DEFAULT_TUBE_NAME = 'default'


class BeanstalkcException(Exception): pass
class UnexpectedResponse(BeanstalkcException): pass
class CommandFailed(BeanstalkcException): pass
class DeadlineSoon(BeanstalkcException): pass

class SocketError(BeanstalkcException):
    @staticmethod
    def wrap(wrapped_function, *args, **kwargs):
        try:
            return wrapped_function(*args, **kwargs)
        except socket.error:
            err = sys.exc_info()[1]
            raise SocketError(err)


class Connection(object):
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, parse_yaml=True,
                 connect_timeout=socket.getdefaulttimeout()):
        if parse_yaml is True:
            try:
                parse_yaml = __import__('yaml').load
            except ImportError:
                logging.error('Failed to load PyYAML, will not parse YAML')
                parse_yaml = False
        self._connect_timeout = connect_timeout
        self._parse_yaml = parse_yaml or (lambda x: x)
        self.host = host
        self.port = port
        self.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self):
        """Connect to beanstalkd server."""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(self._connect_timeout)
        SocketError.wrap(self._socket.connect, (self.host, self.port))
        self._socket.settimeout(None)
        self._socket_file = self._socket.makefile('rb')

    def close(self):
        """Close connection to server."""
        try:
            self._socket.sendall(b'quit\r\n')
        except socket.error:
            pass
        try:
            self._socket.close()
        except socket.error:
            pass

    def reconnect(self):
        """Re-connect to server."""
        self.close()
        self.connect()

    def _interact(self, command, expected_ok, expected_err=[]):
        assert isinstance(command, bytes), 'command must be a bytes instance'
        SocketError.wrap(self._socket.sendall, command)
        status, results = self._read_response()
        if status in expected_ok:
            return results
        elif status in expected_err:
            raise CommandFailed(command.split()[0], status, results)
        else:
            raise UnexpectedResponse(command.split()[0], status, results)

    def _read_response(self):
        line = SocketError.wrap(self._socket_file.readline)
        if not line:
            raise SocketError()
        response = line.split()
        return response[0], response[1:]

    def _read_body(self, size):
        body = SocketError.wrap(self._socket_file.read, size)
        SocketError.wrap(self._socket_file.read, 2)  # trailing crlf
        if size > 0 and not body:
            raise SocketError()
        return body

    def _interact_value(self, command, expected_ok, expected_err=[]):
        return self._interact(command, expected_ok, expected_err)[0]

    def _interact_job(self, command, expected_ok, expected_err, reserved=True):
        jid, size = self._interact(command, expected_ok, expected_err)
        body = self._read_body(int(size))
        return Job(self, int(jid), body, reserved)

    def _interact_yaml(self, command, expected_ok, expected_err=[]):
        size, = self._interact(command, expected_ok, expected_err)
        body = self._read_body(int(size))
        return self._parse_yaml(body)

    def _interact_peek(self, command):
        try:
            return self._interact_job(command, [b'FOUND'], [b'NOT_FOUND'], False)
        except CommandFailed:
            return None

    # -- public interface --

    def put(self, body, priority=DEFAULT_PRIORITY, delay=0, ttr=DEFAULT_TTR):
        """Put a job into the current tube. Returns job id."""
        assert isinstance(body, bytes), 'Job body must be a bytes instance'
        jid = self._interact_value(b'put %d %d %d %d\r\n%s\r\n' % (
                                       priority, delay, ttr, len(body), body),
                                   [b'INSERTED'],
                                   [b'JOB_TOO_BIG', b'BURIED', b'DRAINING'])
        return int(jid)

    def reserve(self, timeout=None):
        """Reserve a job from one of the watched tubes, with optional timeout
        in seconds. Returns a Job object, or None if the request times out."""
        if timeout is not None:
            command = b'reserve-with-timeout %d\r\n' % timeout
        else:
            command = b'reserve\r\n'
        try:
            return self._interact_job(command,
                                      [b'RESERVED'],
                                      [b'DEADLINE_SOON', b'TIMED_OUT'])
        except CommandFailed:
            exc = sys.exc_info()[1]
            _, status, results = exc.args
            if status == b'TIMED_OUT':
                return None
            elif status == b'DEADLINE_SOON':
                raise DeadlineSoon(results)

    def kick(self, bound=1):
        """Kick at most bound jobs into the ready queue."""
        return int(self._interact_value(b'kick %d\r\n' % bound, [b'KICKED']))

    def kick_job(self, jid):
        """Kick a specific job into the ready queue."""
        self._interact(b'kick-job %d\r\n' % jid, [b'KICKED'], [b'NOT_FOUND'])

    def peek(self, jid):
        """Peek at a job. Returns a Job, or None."""
        return self._interact_peek(b'peek %d\r\n' % jid)

    def peek_ready(self):
        """Peek at next ready job. Returns a Job, or None."""
        return self._interact_peek(b'peek-ready\r\n')

    def peek_delayed(self):
        """Peek at next delayed job. Returns a Job, or None."""
        return self._interact_peek(b'peek-delayed\r\n')

    def peek_buried(self):
        """Peek at next buried job. Returns a Job, or None."""
        return self._interact_peek(b'peek-buried\r\n')

    def tubes(self):
        """Return a list of all existing tubes."""
        return self._interact_yaml(b'list-tubes\r\n', [b'OK'])

    def using(self):
        """Return the tube currently being used."""
        return self._interact_value(b'list-tube-used\r\n', [b'USING'])

    def use(self, name):
        """Use a given tube."""
        return self._interact_value(b'use %s\r\n' % name, [b'USING'])

    def watching(self):
        """Return a list of all tubes being watched."""
        return self._interact_yaml(b'list-tubes-watched\r\n', [b'OK'])

    def watch(self, name):
        """Watch a given tube."""
        return int(self._interact_value(b'watch %s\r\n' % name, [b'WATCHING']))

    def ignore(self, name):
        """Stop watching a given tube."""
        try:
            return int(self._interact_value(b'ignore %s\r\n' % name,
                                            [b'WATCHING'],
                                            [b'NOT_IGNORED']))
        except CommandFailed:
            # Tried to ignore the only tube in the watchlist, which failed.
            return 0

    def stats(self):
        """Return a dict of beanstalkd statistics."""
        return self._interact_yaml(b'stats\r\n', [b'OK'])

    def stats_tube(self, name):
        """Return a dict of stats about a given tube."""
        return self._interact_yaml(b'stats-tube %s\r\n' % name,
                                   [b'OK'],
                                   [b'NOT_FOUND'])

    def pause_tube(self, name, delay):
        """Pause a tube for a given delay time, in seconds."""
        self._interact(b'pause-tube %s %d\r\n' % (name, delay),
                       [b'PAUSED'],
                       [b'NOT_FOUND'])

    # -- job interactors --

    def delete(self, jid):
        """Delete a job, by job id."""
        self._interact(b'delete %d\r\n' % jid, [b'DELETED'], [b'NOT_FOUND'])

    def release(self, jid, priority=DEFAULT_PRIORITY, delay=0):
        """Release a reserved job back into the ready queue."""
        self._interact(b'release %d %d %d\r\n' % (jid, priority, delay),
                       [b'RELEASED', 'BURIED'],
                       [b'NOT_FOUND'])

    def bury(self, jid, priority=DEFAULT_PRIORITY):
        """Bury a job, by job id."""
        self._interact(b'bury %d %d\r\n' % (jid, priority),
                       [b'BURIED'],
                       [b'NOT_FOUND'])

    def touch(self, jid):
        """Touch a job, by job id, requesting more time to work on a reserved
        job before it expires."""
        self._interact(b'touch %d\r\n' % jid, [b'TOUCHED'], [b'NOT_FOUND'])

    def stats_job(self, jid):
        """Return a dict of stats about a job, by job id."""
        return self._interact_yaml(b'stats-job %d\r\n' % jid,
                                   [b'OK'],
                                   [b'NOT_FOUND'])


class Job(object):
    def __init__(self, conn, jid, body, reserved=True):
        self.conn = conn
        self.jid = jid
        self.body = body
        self.reserved = reserved

    def _priority(self):
        stats = self.stats()
        if isinstance(stats, dict):
            return stats['pri']
        return DEFAULT_PRIORITY

    # -- public interface --

    def delete(self):
        """Delete this job."""
        self.conn.delete(self.jid)
        self.reserved = False

    def release(self, priority=None, delay=0):
        """Release this job back into the ready queue."""
        if self.reserved:
            self.conn.release(self.jid, priority or self._priority(), delay)
            self.reserved = False

    def bury(self, priority=None):
        """Bury this job."""
        if self.reserved:
            self.conn.bury(self.jid, priority or self._priority())
            self.reserved = False

    def kick(self):
        """Kick this job alive."""
        self.conn.kick_job(self.jid)

    def touch(self):
        """Touch this reserved job, requesting more time to work on it before
        it expires."""
        if self.reserved:
            self.conn.touch(self.jid)

    def stats(self):
        """Return a dict of stats about this job."""
        return self.conn.stats_job(self.jid)


if __name__ == '__main__':
    import nose
    nose.main(argv=['nosetests', '-c', '.nose.cfg', '-l', 'DEBUG', '--debug-log', '/tmp/log_nose.log'])
    #conn = Connection(host=b'localhost', port=11300)
    #print(u'conn', conn)
    #tubes = conn.tubes()
    #print(tubes)
    #conn.put(b'hello');
    #job = conn.reserve()
    #print(job)
    #print(job.body)
    #job.delete()
