# knocker
Python 3 utility to help with CTF or boot2root challenges that involve port knocking

Requires argparse.
```
pip install argparse
``` 

```
$ python knocker.py -h
usage: knocker.py [-h] [-c CLOAKED] (-b | -r RANGE | -p PORTS) dest_ip

Tool to interact with ports cloaked with port knocking. Specify either -p or
-r, and a target IP. -c can be used for success checking if the cloaked port
is known.

positional arguments:
  dest_ip               Target host IP that makes use of port knocking

optional arguments:
  -h, --help            
                        show this help message and exit
  -c CLOAKED, --cloaked CLOAKED
                        Specify the target cloaked port for success checking
  -b, --bruteforce      
                        Have knocker automatically brute force the target for you
  -r RANGE, --range RANGE
                        Specify a suspected range of ports to attempt to brute force (i.e. 1000-1200)
  -p PORTS, --ports PORTS
                        Comma separated list of ports to knock (in proper order)
```
