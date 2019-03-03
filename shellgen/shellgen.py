#!/usr/bin/env python
import os
import sys
import argparse
import socket
import fcntl
import struct

# Directory that contains all the shells
SHELLDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'shells')

# Possible shellnames to use
POSSIBLE_SHELLS = sorted([a.split('.')[0] for a in os.listdir(SHELLDIR) 
        if a.endswith('.shell')])


def get_default_network_interface():
    """
    Returns the default network interface name if possible. Otherwise returns
    None.
    """
    if sys.platform == 'linux' or sys.platform == 'linux2':
        # Read from linux /proc location
        route = "/proc/net/route"
        with open(route, 'r') as f:
            for line in f.read().splitlines():
                try:
                    network_iface, dest, _, flags, _, _, _, _, _, _, _ = line.strip().split()
                    if dest != '00000000' or not int(flags, 16) & 2:
                        continue
                    return network_iface
                except:
                    continue
    return None

def get_ip_address(network_iface):
    """
    Returns the ip address of a specific network interface. Returns None if
    it could not be determined.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(), 0x8915, struct.pack('256s', network_iface[:15].encode('utf-8'))
        )[20:24])
    except:
        return None


def print_shells():
    """
    Prints list of possible shells.
    """
    sys.stdout.write("Possible shells:\n")
    sys.stdout.write("-" * 45 + '\n')
    for i, k in enumerate(POSSIBLE_SHELLS):
        sys.stdout.write('{:15}'.format(k))
        if i > 0 and i % 3 == 0:
            sys.stdout.write('\n')
        elif i == len(POSSIBLE_SHELLS) - 1:
            sys.stdout.write('\n')



def print_version():
    """
    Print version information.
    """
    sys.stdout.write('Shellgen {}\n'.format(__version__))


def get_shell_from_file(shellname):
    """
    Returns the shell from a .shell file in the shell directory as a string. It
    can then be formatted to place ip and port in the file.
    """
    filecontents = None
    with open('shells/{}.shell'.format(shellname), 'r') as f:
        filecontents = f.read()
    return filecontents


def gen_shell(shellname, ip, port):
    """
    Returns reverse shell code with ip addresses and ports filled in.
    """
    return get_shell_from_file(shellname).format(ipaddress=ip, port=port)


def main():
    """
    Generate the shell and checks the input. Writes to file if -o is specified.
    """

    # Argument parser
    EXAMPLE_USAGE = """Example usage:\n\n
        ./shellgen.py -I tun0 -p 9234 -o shell.sh tcpbash
    """
    parser = argparse.ArgumentParser(
            description="""Generates a reverse shell in multiple languages. 
            Shells are from Pentestmonkey which are listed here: 
            http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet
            """, epilog=EXAMPLE_USAGE)

    parser.add_argument('shell', nargs=(1 if '--list' not in sys.argv and 
            '--version' not in sys.argv else '?'), metavar='SHELL', type=str,
            help="""What type of reverse shell to output. For a list of possible
            types use --list.""")

    parser.add_argument('--list', dest='list', default=False, 
            action='store_true', help="""Prints a list of possible type of 
            reverse shells this script can generate. You can add custom shells 
            in the shells/ directory.""")
    parser.add_argument('-i', '--ip-address', metavar="ADDRESS", 
            dest='ipaddress', type=str, default=None, help="""IP address for the
            reverse shell. Should be 
            used if you don't want the script to automatically determine the ip
            address.""")
    parser.add_argument('-p', '--port', dest='port', type=int, default=1234,
            help="""The port to use for the reverse shell. Default is 1234.""")
    parser.add_argument('-I', '--interface', dest='interface', type=str, 
            default=get_default_network_interface(), help="""The network 
            interface to get the IP address from. Will only be used of no IP 
            address provided. Example: eth0. Will automatically determine 
            when not provided.""")
    parser.add_argument('-o', '--output', dest='outputfile', type=str, 
            default=None, help="""File to output the shell to. If not provided,
            it will be printed to stdout.""")
    parser.add_argument('--version', dest='version', default=False,
            action='store_true', help="""Print version""")
            
    args = parser.parse_args()

    # List possible shells
    if args.list:
        print_shells()
        sys.exit(0)

    if args.version:
        print_version()
        sys.exit(0)

    # Determine ip address
    ipaddress = None
    if not args.ipaddress or len(args.ipaddress) == 0:
        iface = None
        if not args.interface:
            # Determine interface automatically
            iface = get_default_network_interface()
            if not iface:
                parser.error("""Interface could not be determined. Please specify
                    an interface yourself, or specify an IP address.""")
        else:
            iface = args.interface

        # Determine ip based on interface
        ipaddress = get_ip_address(iface)
        if not ipaddress:
            parser.error("""IP address could not be determined. Please use 
                the -i argument to specify the ip address yourself.""")
    else:
        ipaddress = args.ipaddress

    if args.shell[0] in POSSIBLE_SHELLS:
        shellname = args.shell[0]
    else:
        parser.error("""Invalid shell name '{}'. Use --list to show a list of 
            possible shellnames.""".format(args.shell[0]))

    shellcode = gen_shell(shellname, ipaddress, args.port)

    if args.outputfile:
        with open(args.outputfile, 'w') as f:
            f.write(shellcode + '\n')
        sys.stdout.write('Shellcode written to file \'{}\'\n'.format(
            args.outputfile
        ))
    else:
        sys.stdout.write(shellcode + '\n')
    sys.exit(0)
