"""
Scan open TCP ports.

Just for fun, for more serious tasks use nmap, e.g.:
    nmap -p 22 --open -sV 192.168.1.0/24
"""
import threading
import socket
import concurrent.futures

_meta_shell_command = 'port_scanner'

REPL = '{}'
PORTS = [22, 80, 8000]

def str_gen(base, gens):
    if len(gens) == 0:
        return base

    found = False

    rv = []
    gen = gens.pop()
    for bstr in base:
        if REPL in bstr:
            found = True
            i = bstr.find(REPL)
            j = i + len(REPL)
            for gg in gen:
                rv.append(bstr[0:i] + str(gg) + bstr[j:])
        else:
            rv.append(bstr)

    if found:
        return str_gen(rv, gens)

    return rv 

def try_connect_tcp(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)

    port = int(ip.split(':')[1])
    ip_cut = ip.split(':')[0]

    try:
        sock.connect((ip_cut, port))
        sock.close()
    except OSError as ex:
        return False, ip

    print(f'Found at {ip}.')
    return True, ip

if __name__ == '__main__':
    base = '192.168.%s.%s:%s'.replace('%s', REPL) 
    print(f'Start scan using {base}.')

    ip_nums = [i for i in range(0, 256)]

    futures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        for st in str_gen([base], [PORTS, ip_nums, ip_nums]):
            future = executor.submit(try_connect_tcp, st)
            futures.append(future)

    print('=' * 40)
    for future in futures:
        rv, ip = future.result()
        if rv:
            print(f'Found at {ip}.')
        else:
            if False:
                print(f'Not found at {ip}.')

