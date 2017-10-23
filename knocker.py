#!/usr/bin/python3

import argparse

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

def brute_force_range(dest_ip, port_range, cloaked_port):
    for port in range(int(port_range[0]), int(port_range[1])+1):
        knock(dest_ip, port)
    if cloaked_port != None:
        if not test_target(dest_ip, cloaked_port):
            brute_force_range(dest_ip, port_range, cloaked_port)
        else:
            print("Target port {} opened!".format(cloaked_port))

def main():
    parser = argparse.ArgumentParser(description="Tool to interact with ports cloaked with port knocking. Specify either -p or -r, and a target IP. -c can be used for success checking if the cloaked port is known.")
    run_mode = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("dest_ip", help="Target host IP that makes use of port knocking")
    parser.add_argument("-c", "--cloaked", help="Specify the target cloaked port for success checking")
    run_mode.add_argument("-b", "--bruteforce", help="Have knocker automatically brute force the target for you", action="store_true")
    run_mode.add_argument("-r", "--range", help="Specify a suspected range of ports to attempt to brute force (i.e. 1000-1200)")
    run_mode.add_argument("-p", "--ports", help="Comma separated list of ports to knock (in proper order)")
    args = parser.parse_args()

    if args.ports != None:
        port_list = args.ports.split(',')
        known_knock_order(args.dest_ip, port_list, args.cloaked)
    else:
        if args.range != None:
            port_range = args.range.split('-')
        else:
            port_range = ['1','65535']
        brute_force_range(args.dest_ip, port_range, args.cloaked)

if __name__ == '__main__':
    main()
