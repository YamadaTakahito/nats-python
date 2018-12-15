import asyncio
import signal
import sys

from settings import SUB, NATS_URL

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers


@asyncio.coroutine
def closed_cb():
    print("Connection to NATS is closed.")
    yield from asyncio.sleep(0.1, loop=loop)
    loop.stop()


@asyncio.coroutine
def reconnected_cb():
    print("Connected to NATS at {}...".format(nc.connected_url.netloc))


def sub(loop):
    nc = NATS()

    options = {
        "io_loop": loop,
        "closed_cb": closed_cb,
        "reconnected_cb": reconnected_cb,
        "servers": NATS_URL
    }
    yield from nc.connect(**options)
    print("Connected to NATS at {}...".format(nc.connected_url.netloc))

    def signal_handler():
        if nc.is_closed:
            return
        print("Disconnecting...")
        loop.create_task(nc.close())
    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)

    async def help_request(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))
<<<<<<< HEAD
        await nc.publish(reply, b'BBB')
=======
        await nc.publish(reply, b'AAA')
>>>>>>> e5cecba08fbc168199fd486b4821be94d4872e7b

    yield from nc.subscribe(SUB, cb=help_request)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sub(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()
