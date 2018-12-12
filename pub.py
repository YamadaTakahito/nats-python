import asyncio
import signal

from settings import SUB

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers

NATS_URL = "demo.nats.io:4222"


def pub(msg):
    async def p(msg):
        nc = NATS()
        await nc.connect(NATS_URL)
        await nc.publish(SUB, msg.encode('utf-8'))
        await nc.flush()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(p(msg))
