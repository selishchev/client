import socket
import time


class Client:

    def __init__(self, host, port, timeout=None):
        self.sock = socket.create_connection((host, int(port)), timeout)

    def put(self, name, value, timestamp=None):
        a = '\n'
        value = str(value)
        if not timestamp:
            timestamp = str(int(time.time()))
        else:
            timestamp = str(timestamp)
        with self.sock as sock:
            comm = 'put ' + name + ' ' + value + ' ' + timestamp + a
            try:
                sock.sendall(comm.encode('utf-8'))
                data = sock.recv(1024)
                dat = data.decode('utf-8')
                if dat == 'ok' + a + a:
                    print(dat)
                else:
                    print('error' + a + 'wrong command' + a + a)
            except:
                raise ClientError

    def get(self, key):
        a = '\n'
        keys = []
        values = []
        dct = {}
        with self.sock as sock:
            comm = 'get ' + key + a
            sock.sendall(comm.encode('utf-8'))
            data = sock.recv(1024)
            dat = data.decode('utf-8')
            try:
                dat = dat.split('\n')
                for key in dat[1:]:
                    if len(key) != 0:
                        metric, value, timestamp = key.split()
                        keys.append(metric)
                        values.append((int(timestamp), float(value)))
                for i, j in zip(keys, values):
                    if i not in dct.keys():
                        dct[i] = []
                        dct[i].append(j)
                    else:
                        dct[i].append(j)
                for v in dct.values():
                    v.sort(key=lambda x: x[0])
            except:
                raise ClientError
        return dct


class ClientError(Exception):

    def __init__(self):
        super().__init__()
