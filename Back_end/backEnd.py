import argparse
import socket
import netifaces
import ipaddress
from concurrent.futures import ThreadPoolExecutor, wait
from pprint import pp
import time
import pika
import requests
import sys
import mysql.connector as mysql
import psycopg2

# Source: https:///stackoverflow.com/questions/26174743/making-a-fast-port-scanner
def tcp_connect(ip, port_number):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(0.5)
    try:
        TCPsock.connect((ip, port_number))
        return True
    except:
        return False

# Parse command line arguments
parser = argparse.ArgumentParser(
        description="Tests containers found on the network")
parser.add_argument('-i', help="interface to scan", metavar="INTERFACE",
        default='eth0')
parser.add_argument('-t', help="maximum threads to use", metavar="THREADS",
        default=1000)
args = parser.parse_args()
interface = args.i
threads = args.t

pool = ThreadPoolExecutor(threads)

########################### Host Discovery ####################################

print(f"Discovering hosts on {interface}...")

hosts = {}
ports = {
    3306 : 'MySQL/MariaDB',
    5432 : 'PostgreSQL',
    5672 : 'RabbitMQ',
}

# create a network of all valid IPs
ipv4if = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]
ourip = ipv4if['addr']
netmask = ipv4if['netmask']
network = ipaddress.ip_network((ourip, netmask), strict=False)

# create threads to check the services of hosts
for addr in network:
    ip = str(addr)
    hosts[ip] = {}
    for port, service in ports.items():
        hosts[ip][service] = pool.submit(tcp_connect, ip, port)

# store the results of each thread
count = 0
for ip in hosts:
    if (count % 10000) == 0:
        print(f"> {count}/{len(hosts)} hosts scanned...")
    for service in hosts[ip]:
        future = hosts[ip][service]
        wait([future])
        hosts[ip][service] = future.result()
    count += 1

# filter out hosts that don't have any services and make a services list
active_hosts = {}
for ip in hosts:
    services = []
    for service in hosts[ip]:
        if hosts[ip][service]:
            services.append(service)
    if len(services) > 0:
        active_hosts[ip] = services

# print the output
pp(active_hosts)

# quit if we have nothing to test
if len(active_hosts) == 0:
    print("No active hosts! Is this running on the correct network?")
    sys.exit(1)

