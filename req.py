import asyncio
import signal

from settings import SUB, NATS_URL

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout

TIME_OUT = 1


async def req(loop):
    nc = NATS()
    messages = []

    await nc.connect(NATS_URL, loop=loop)

    async def request_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))

        messages.append(data)

    # Signal the server to stop sending messages after we got 10 already.
    await nc.request(
        SUB, b'help', TIME_OUT, expected=2, cb=request_handler)

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
    return messages


def get_messages():
    loop = asyncio.get_event_loop()
    msgs = loop.run_until_complete(req(loop))
    loop.close()
    print(msgs)


if __name__ == '__main__':
    get_messages()
