import asyncio
import signal

from settings import SUB, NATS_URL

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout

TIME_OUT = 10


@asyncio.coroutine
def closed_cb():
    print("Connection to NATS is closed.")
    yield from asyncio.sleep(0.1, loop=loop)
    loop.stop()


@asyncio.coroutine
def reconnected_cb():
    print("Connected to NATS at {}...".format(nc.connected_url.netloc))


async def req(loop, msg):
    nc = NATS()

    options = {
        "io_loop": loop,
        "closed_cb": closed_cb,
        "reconnected_cb": reconnected_cb,
        "servers": NATS_URL
    }
    await nc.connect(**options)

    try:
        res = await nc.request(SUB, msg.encode('utf-8'), TIME_OUT)
        print("Received response: {}".format(res.data.decode()))
    except ErrTimeout:
        print("Flush timeout")

    await nc.close()


if __name__ == '__main__':
    msg = 'sample message'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(req(loop, msg))
    loop.close()
