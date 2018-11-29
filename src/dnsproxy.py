#!/usr/bin/env python3.6

import logging
import signal
import configparser
from datetime import datetime
from time import sleep

from dnslib import RR, QTYPE, A, dns, DNSHeader, DNSQuestion
from dnslib.proxy import ProxyResolver
from dnslib.server import DNSServer, DNSRecord

class Resolver(ProxyResolver):
    def __init__(self, address, blacklist):
        self.blacklist = blacklist.split(", ")
        self.response = config['Proxy']['response']
        super().__init__(address, 53, 5)

    def resolve(self, request, handler):
        qname = request.q.qname
        
        if (self.blacklisted(qname, self.blacklist)):
            reply = request.reply()
            reply.add_answer(RR(qname,QTYPE.A,ttl=300,rdata=A(self.response)))
            print(reply)
            return reply
        else:
            return super().resolve(request, handler)

    def blacklisted(self, domain, blacklist):
        if domain in blacklist:
            return self.response
        else:
            return ""

def handle_sig(signum, frame):
    exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, handle_sig)

    config = configparser.ConfigParser()
    config.read('config.ini')
    
    port = int(config['Proxy']['port'])
    dns_server = config['DNS']['ip']
    blacklist = config['Proxy']['blacklist']
    resolver = Resolver(dns_server, blacklist)
    proxy_server = DNSServer(resolver, port=port)


    print('starting DNS server on port ' + str(port) + ', upstream DNS server \"' + dns_server + '"')
    proxy_server.start_thread()

    try:
        while proxy_server.isAlive():
            sleep(1)
    except KeyboardInterrupt:
        pass