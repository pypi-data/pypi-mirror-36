from __future__ import print_function
import sys
import time
import functools

import zope.interface
from twisted.python import usage, log
from twisted.plugin import IPlugin
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.endpoints import serverFromString
from twisted.web.http import HTTPChannel
from twisted.web.static import Data
from twisted.web.resource import Resource
from twisted.web.server import Site

from carml import util
import txtorcon
from txtorcon import TCPHiddenServiceEndpoint


async def run(reactor, cfg, tor, ports, version):

    print("Creating v{} onion-service...".format(version))
    def update(pct, tag, description):
        print("  {}: {}".format(util.pretty_progress(pct), description))
    hs = await tor.create_onion_service(ports, version=version, progress=update, await_all_uploads=True)
    # print("At least one HSDir successful")
    print("published to all HSDirs")

    async def remove():
        print("removing onion-service")
        await hs.remove()
    reactor.addSystemEventTrigger('before', 'shutdown', remove)

    print("Running an Onion Service mapping the following ports:")
    for port in ports:
        if isinstance(port, tuple):
            remote_port, local_port = port
        else:
            remote_port, local_port = port, port

        print(
            "{}:{} (remote) -> {} (local)".format(
                hs.hostname,
                remote_port,
                local_port,
            )
        )

    # we never callback() on this, so we serve forever
    await Deferred()
