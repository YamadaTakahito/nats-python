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


async def req(loop):
    nc = NATS()

    options = {
        "io_loop": loop,
        "closed_cb": closed_cb,
        "reconnected_cb": reconnected_cb,
        "servers": NATS_URL
    }
    await nc.connect(**options)

    async def request_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))

    # Signal the server to stop sending messages after we got 10 already.
    await nc.request(
        SUB, b'help', expected=3, cb=request_handler)

    try:
        # Flush connection to server, returns when all messages have been processed.
        # It raises a timeout if roundtrip takes longer than 1 second.
        await nc.flush(1)
    except ErrTimeout:
        print("Flush timeout")

    await asyncio.sleep(5, loop=loop)

    # Drain gracefully closes the connection, allowing all subscribers to
    # handle any pending messages inflight that the server may have sent.
    await nc.drain()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(req(loop))
    loop.close()
