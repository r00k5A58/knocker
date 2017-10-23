#!/usr/bin/python3

##############################################################################
#
#  Created by Derek Rook https://github.com/r00k5A58
#  10/23/2017
#  Small tool to interact with hosts using port knocking as a security measure
#  TODO: Create full brute force mode that looks for filtered ports on target
#        then runs full brute force mode until filtered ports are open.
#        Obviously shouldn't be ran against firewalls :P
#
##############################################################################

import argparse

from sys import exit
from socket import socket, AF_INET, SOCK_STREAM

def knock(dest_ip, dest_port):
    send_knock = socket(AF_INET, SOCK_STREAM)
    try:
        send_knock.connect((dest_ip, int(dest_port)))
        send_knock.shutdown()
        send_knock.close()
    except:
        pass

def test_target(dest_ip, cloaked_port):
    cloak_connect = socket(AF_INET, SOCK_STREAM)
    try:
        cloak_connect.connect((dest_ip, int(cloaked_port)))
        cloak_connect.close()
        return True
    except:
        return False

def known_knock_order(dest_ip, port_list, cloaked_port):
    for port in port_list:
        knock(dest_ip, port)
    if cloaked_port != None:
        if test_target(dest_ip, cloaked_port):
            print("Target port {} opened!".format(cloaked_port))

def brute_force_range(dest_ip, port_range, cloaked_port, maxlen):
    retry_counter = 0
    while retry_counter < maxlen:
        print("Starting iteration {0} for range {1}-{2}".format(retry_counter+1, port_range[0], port_range[1]))
        for port in range(int(port_range[0]), int(port_range[1])+1):
            knock(dest_ip, port)
        if not test_target(dest_ip, cloaked_port):
            retry_counter += 1
        else:
            exit("Target port {} opened!".format(cloaked_port))
    if not test_target(dest_ip, cloaked_port):
        exit("Brute force failed. Time for more recon")

def main():
    parser = argparse.ArgumentParser(description="Tool to interact with ports cloaked with port knocking. Specify -p, -r, or -b, and a target IP. -c can be used for success checking if the cloaked port is known.\n\nRequires root or sudo privileges for socket creation.")
    run_mode = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("dest_ip", help="Target host IP that makes use of port knocking")
    parser.add_argument("-c", "--cloaked", help="Specify the target cloaked port for success checking")
    parser.add_argument("-m", "--maxlen", help="Specify the max iterations a brute force will run before assuming failure (default 10)", type=int, default=10)

    run_mode.add_argument("-b", "--bruteforce", help="Have knocker automatically brute force the target for you. Shortcut for -r 1-65535", action="store_true")
    run_mode.add_argument("-r", "--range", help="Specify a suspected range of ports to attempt to brute force (i.e. 1000-1200)")
    run_mode.add_argument("-p", "--ports", help="Comma separated list of ports to knock (in proper order)")

    args = parser.parse_args()

    if args.ports != None:
        port_list = args.ports.split(',')
        known_knock_order(args.dest_ip, port_list, args.cloaked)
    else:
        if args.range != None and args.cloaked != None:
            port_range = args.range.split('-')
        elif args.bruteforce and args.cloaked != None:
            port_range = ['1','65535']
        elif args.cloaked == None:
            print("When using a brute force option (-r or -b), the target cloaked port should be specified.\n".upper())
            parser.print_help()
            exit()
        brute_force_range(args.dest_ip, port_range, args.cloaked, args.maxlen)

if __name__ == '__main__':
    main()
