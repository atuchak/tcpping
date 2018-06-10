# tcpping
The Python way to ping a server through TCP and get statistics (```ping()```). 
and wait until your server is up (```wait_for_ping()```).

## Usage


```
pip install tcpping2
```

```python
from tcpping2 import Ping
ping = Ping('google.com', 80, interval=0.1, timeout=1)
ping.ping(3)
Out[4]: 
{'average': 22.462,
 'conn_times': [27.744084014557302, 19.244000897742808, 20.39720898028463],
 'maximum': 27.744,
 'minimum': 19.244,
 'n': 3,
 'success_rate': 100.0}
 ```
 
```python
from tcpping2 import Ping

ping = Ping('google.com', 80)
ping.wait_for_ping(blocking_timeout=2)
# do somethitg with your server
```

```python
from tcpping2 import Ping
ping = Ping('google.com', 1234) # the port number which not exists on the server
ping.wait_for_ping(blocking_timeout=2)
Traceback (most recent call last):
  File "tcpping2/__init__.py", line 124, in wait_for_ping
    raise BlockingTimeoutError
tcpping2.BlockingTimeoutError
```

## Contributors
* Anton Tuchak ([atuchak](https://github.com/atuchak))