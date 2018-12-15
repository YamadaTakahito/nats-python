import asyncio
import signal

from settings import SUB, NATS_URL

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout

TIME_OUT = 1


async def req(loop, msg):
    nc = NATS()
    messages = []

    await nc.connect(NATS_URL, loop=loop)

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
    print(msgs)
