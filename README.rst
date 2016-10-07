.. -*- coding: utf-8; indent-tabs-mode:nil; -*-

######
Suidao
######

This package contains network tunneling stuff.
For now, we have:

- ``htc.py`` and ``hts.py`` that are very much inspired from
  `HTTPTunnel <https://github.com/larsbrinkhoff/httptunnel>`_,
  which I couldn't get to work over proxies.


HTC & HTS
#########

``htc.py`` provides an stdio pipe, and can be used with SSH with a
config along the lines of::

  ProxyCommand htc.py http://my.domain.tld/path/to/subdir/$(date +%%Y%%m%%dT%%H%%M%%S)

``hts.py`` would be the server side of this, and is currently
hard-coded to connect to the local ssh port.

The code of htc/hts is intended to remain very short, for auditing
purposes.

The server side needs flask, the client side needs requests.

