import pytest

from tcpping2 import Ping, BlockingTimeoutError


def test_tcpping_ping():
    ping = Ping('google.com', 80, interval=0.1, timeout=1)
    res = ping.ping(2)

    assert isinstance(res, dict)
    assert 'maximum' in res
    assert 'success_rate' in res
    assert 'conn_times' in res
    assert 'n' in res
    assert 'average' in res
    assert 'minimum' in res


def test_tcpping_wait_for():
    ping = Ping('google.com', 80)
    ping.wait_for_ping(blocking_timeout=2)

    ping = Ping('google.com', 8888)
    with pytest.raises(BlockingTimeoutError):
        ping.wait_for_ping(blocking_timeout=2)
