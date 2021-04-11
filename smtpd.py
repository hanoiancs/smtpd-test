import asyncio

from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Sink, Debugging

class ExampleHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        # if not address.endswith('@example.com'):
        #     return '550 not relaying to that domain'
        
        envelope.rcpt_tos.append(address)

        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        print('Message from %s' % envelope.mail_from)
        print('Message for %s' % envelope.rcpt_tos)
        print('Message data:\n')
        # for ln in envelope.content.decode('utf', errors='replace').splitlines():
        #     print(f'> {ln}'.strip())
        print(envelope.content.decode('utf', errors='replace'))
        print()
        print('End of message')
        return '250 Message accepted for delivery'


async def amain(loop):
    handler = ExampleHandler()
    ctrl = Controller(handler=handler, ready_timeout=10, hostname='127.0.0.1')
    ctrl.start()
    print(ctrl.hostname, ctrl.port)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(amain(loop=loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
