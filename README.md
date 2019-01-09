DNS Proxy on Python3
========

DNS proxy server with blacklist test task, written on Python 3.2

## Requirements

DNS proxy requires Python3 and pip for Python3 to be installed:
```bash
$ sudo apt-get install python3 python3-pip
```
## Clone & Run

```bash
$ git clone https://github.com/nevmnd/dnsproxy_py.git
$ cd dnsproxy_py/src
$ python3 dnsproxy.py
```
## Usage

You can check its work by typing:
```bash
$ dig -p 5300 google.ru
```
but be sure to turn off your local DNS server before that.

## Proxy configuration

Section "DNS" contains options of upstream DNS server (IP and port).
Section "Proxy" contains 3 options:
  - Address of local port which it should be run on to. 
  - IP of server where proxy should redirect queries. If that address not specified, proxy will answer with empty response.
  - List of domains which proxy should block are defined in section "Blacklist".
