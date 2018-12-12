import asyncio
import signal

from settings import SUB, NATS_URL

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout


async def req(loop):
    nc = NATS()

    await nc.connect(NATS_URL, loop=loop)

    try:
        response = await nc.request("{}.1".format(SUB), b'help me', 0.6)
        print("Received response: {message}".format(
            message=response.data.decode()))
    except ErrTimeout:
        print("Request timed out")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(req(loop))
    loop.close()
