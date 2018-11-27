#!/usr/bin/env python3.6

import logging
import signal
import configparser
from datetime import datetime
from time import sleep

from dnslib import QTYPE, RR, dns
from dnslib.proxy import ProxyResolver
from dnslib.server import DNSServer, DNSRecord

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s', datefmt='%H:%M:%S'))

logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class Resolver(ProxyResolver):
    def __init__(self, dns_server):
        super().__init__(dns_server, 53, 5)

    def resolve(self, request, handler):
        proxy_r = request.send(self.address,self.port,
                                timeout=self.timeout)
        type_name = QTYPE[request.q.qtype]
        #reply = request.reply()
        reply = DNSRecord.parse(proxy_r)
        print (reply)
        return super().resolve(request, handler)
    
    def blacklisted(s, blacklist):
        result=[]
        result = blacklist.split(", ")
        if s in result:
            return config['Proxy']['response']
        else:
            return 0

def handle_sig(signum, frame):
    exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, handle_sig)

    config = configparser.ConfigParser()
    config.read('config.ini')
    
    port = int(config['Proxy']['port'])
    dns_server = config['DNS']['ip']

    resolver = Resolver(dns_server)
    proxy_server = DNSServer(resolver, port=port)


    logger.info('starting DNS server on port %d, upstream DNS server "%s"', port, dns_server)
    proxy_server.start_thread()

    try:
        while proxy_server.isAlive():
            sleep(1)
    except KeyboardInterrupt:
        pass