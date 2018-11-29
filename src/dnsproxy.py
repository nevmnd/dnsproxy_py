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
    def __init__(self, address, port, blacklist, response):
        self.blacklist = blacklist.split(", ")
        self.response = response
        self.address = address
        self.port = port
        super().__init__(address, int(port), 5)

    def resolve(self, request, handler):
        qname = request.q.qname
        if (self.blacklisted(qname, self.blacklist)):
            proxy_r = request.send(self.address, self.port, timeout=5)
            reply = DNSRecord.parse(proxy_r)
            ttl = reply.a.ttl
            reply = request.reply()
            if (self.response):
                reply.add_answer(RR(qname,QTYPE.A,ttl=ttl,rdata=A(self.response)))
            return reply
        else:
            return super().resolve(request, handler)

    def blacklisted(self, domain, blacklist):
        return True if domain in blacklist else False

def handle_sig(signum, frame):
    exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, handle_sig)

    config = configparser.ConfigParser()
    config.read('config.ini')
    
    port = int(config['Proxy']['port'])
    dns_server = config['DNS']['ip']
    dns_port = config['DNS']['port']
    blacklist = config['Proxy']['blacklist']
    try:
        response = config['Proxy']['response']
    except:
        response = ""
    resolver = Resolver(dns_server, dns_port, blacklist, response)
    proxy_server = DNSServer(resolver, port=port)


    print('starting DNS server on port ' + str(port) + ', upstream DNS server \"' + dns_server + '"')
    proxy_server.start_thread()

    try:
        while proxy_server.isAlive():
            sleep(1)
    except KeyboardInterrupt:
        pass