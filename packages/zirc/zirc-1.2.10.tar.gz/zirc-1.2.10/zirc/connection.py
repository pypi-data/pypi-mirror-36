import socket

class Socket(object):
    """
    A class for creating socket connections.

    Creating a connection:
        address = ("irc.stuxnet.xyz", 6697)
        Socket(wrapper=ssl.wrap_socket, family=socket.AF_INET6)(address)
    """
    def __init__(self, wrapper=None, family=socket.AF_INET, socket_class=None, bind_address=None):
        if socket_class is not None:
            self.socket_class = socket_class
            self.sock = socket_class(family, socket.SOCK_STREAM)
        else:
            self.sock = socket.socket(family, socket.SOCK_STREAM)
            self.socket_class = socket_class
        self.family = family
        self.bind_address = bind_address
        self.wrapper = wrapper

    def connect(self, socket_address, keyfile=None, certfile=None):
        self.keyfile = keyfile
        self.certfile = certfile
        if self.wrapper is not None:
            self.sock = self.wrapper(self.sock, keyfile=keyfile, certfile=certfile)
        if self.bind_address:
            self.sock.bind(self.bind_address)
        self.sock.connect(socket_address)

        return self.sock
    __call__ = connect
