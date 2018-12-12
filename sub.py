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


# @asyncio.coroutine
# def subscribe_handler(msg):
#     subject = msg.subject
#     reply = msg.reply
#     data = msg.data.decode('utf-8')

#     print("Received a message on '{subject} {reply}': {data}".format(
#         subject=subject, reply=reply, data=data))


def sub(loop, subject):
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
        data = msg.data.decode('utf-8')
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))
        await nc.publish(reply, b'I can help')

    yield from nc.subscribe(subject, cb=help_request)


if __name__ == '__main__':
    idx = sys.argv[-1]
    subject = "{}.{}".format(SUB, idx)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(sub(loop, subject))
    try:
        loop.run_forever()
    finally:
        loop.close()

    # async def help_request(msg):
    #     subject = msg.subject
    #     reply = msg.reply
    #     data = msg.data.decode()
    #     print("Received a message on '{subject} {reply}': {data}".format(
    #         subject=subject, reply=reply, data=data))
    #     await nc.publish(reply, b'I can help')

    # # Use queue named 'workers' for distributing requests
    # # among subscribers.
    # sid = await nc.subscribe("help", "workers", help_request)
