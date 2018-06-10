import socket

from itertools import zip_longest
from timeit import default_timer as timer

import time

__version__ = '0.1.6'


# Based on https://github.com/zhengxiaowai/tcping

def avg(x):
    return sum(x) / float(len(x))


class BlockingTimeoutError(Exception):
    pass


class Socket:
    def __init__(self, family, type_, timeout):
        s = socket.socket(family, type_)
        s.settimeout(timeout)
        self._s = s

    def connect(self, host, port=80):
        self._s.connect((host, int(port)))

    def shutdown(self):
        self._s.shutdown(socket.SHUT_RD)

    def close(self):
        self._s.close()


class Timer:
    def __init__(self):
        self._start = 0
        self._stop = 0

    def start(self):
        self._start = timer()

    def stop(self):
        self._stop = timer()

    def cost(self, funcs, args):
        self.start()
        for func, arg in zip_longest(funcs, args):
            if arg:
                func(*arg)
            else:
                func()

        self.stop()
        return self._stop - self._start


class Ping:
    def __init__(self, host, port=80, interval=0.5, timeout=1):
        self.timer = Timer()
        self._successed = 0
        self._failed = 0
        self._conn_times = []
        self._host = host
        self._port = port
        self._interval = interval
        self._timeout = timeout

    def _create_socket(self, family, type_):
        return Socket(family, type_, self._timeout)

    def _success_rate(self):
        count = self._successed + self._failed
        try:
            rate = (float(self._successed) / count) * 100
            rate = '{0:.2f}'.format(rate)
        except ZeroDivisionError:
            rate = '0.00'
        return float(rate)

    def statistics(self, n):
        conn_times = self._conn_times if self._conn_times != [] else [0]
        minimum = float('{0:.3f}'.format(min(conn_times)))
        maximum = float('{0:.3f}'.format(max(conn_times)))
        average = float('{0:.3f}'.format(avg(conn_times)))
        success_rate = self._success_rate()
        return {k: v for k, v in locals().items() if k not in {'self'}}

    def ping(self, count=1):
        for _ in range(count):
            s = self._create_socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                cost_time = self.timer.cost(
                    (s.connect, s.shutdown),
                    ((self._host, self._port), None))
                s_runtime = 1000 * cost_time
                self._conn_times.append(s_runtime)
                time.sleep(self._interval)

            except (socket.timeout, ConnectionRefusedError):
                self._failed += 1
            else:
                self._successed += 1
            finally:
                s.close()

        return self.statistics(count)

    def wait_for_ping(self, blocking_timeout=10):
        started_at = time.monotonic()
        while time.monotonic() - started_at < blocking_timeout:
            s = self._create_socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                s.connect(self._host, self._port)
                s.shutdown()
                return
            except (socket.timeout, ConnectionRefusedError):
                time.sleep(self._interval)
            finally:
                s.close()

        raise BlockingTimeoutError
