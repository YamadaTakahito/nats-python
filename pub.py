import asyncio
import signal

from settings import SUB, NATS_URL

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers


def pub(msg):
    async def p(msg):
        nc = NATS()
        await nc.connect(NATS_URL)
        await nc.publish('{}.1'.format(SUB), msg.encode('utf-8'))
        await nc.flush()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(p(msg))


if __name__ == '__main__':
    pub('message')
