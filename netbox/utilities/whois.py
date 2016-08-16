import socket
from collections import defaultdict


def whois(server, query, parsed=True):
    """Make a whois query on port 43, parsed in a dict or as a string. If parsed, the dict has for each present key a list of values."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server, 43))
    sock.send(query + '\r\n')
    response = ''
    while True:
        d = sock.recv(4096)
        response += d
        if d == '':
            break
    sock.close()
    if response.startswith('%'):
        raise ValueError(response[3:])
        return response
    else:
        if not parsed:
            return response
        else:
            parse_list = []

            if response:
                for line in response.split('\n'):
                    if line:
                        linesplit = line.split(':')
                        if line.startswith(' '):
                            parse_list[len(parse_list) - 1][1] += ' ' + line
                        else:
                            if len(linesplit) > 2:
                                linesplit[1] = ':'.join(linesplit[1:])
                            key = linesplit[0]
                            val = linesplit[1].strip()

                            parse_list.append([key, val])

            parsed = defaultdict(list)
            for k, v in parse_list:
                parsed[k].append(v)

            return parsed
