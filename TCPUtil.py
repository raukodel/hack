import struct
import collections

from enum import Enum


FileTupleData = collections.namedtuple("FileData", "data")


class ConnectionType(Enum):
    END_CONNECTION = 0
    SERVER_OK = 1
    CONNECT = 2
    WRITE = 3
    COMMAND = 4
    SEND = 5


def send_status(sock, request):
    request_packed = struct.pack("H", request.value)
    print('>>> Send    >>> send write request: ', request)
    sock.sendall(request_packed)


def receive_status(sock):
    # Receive status data from the server
    type_respond = struct.unpack("H", sock.recv(1024))[0]
    print('<<< Receive <<< data from server: ', ConnectionType(type_respond))
    return type_respond


# FILE
def check_if_file_exist(name):
    try:
        return open(name).read()

    except FileNotFoundError:
        print("File not found!")
        return None


def get_packed(content):
    file_data = FileTupleData(data=str.encode(content))
    return struct.pack(str(len(content)) + "s", *file_data)


def send_size(sock, content):
    content_size = len(content)
    packed_size = struct.pack("H", content_size)

    print('>>> Send    >>> send file size: ', packed_size)
    sock.sendall(packed_size)


def receive_file_size(connection):
    file_size = connection.recv(1024)
    file_size = struct.unpack("H", file_size)[0]
    print('<<< Receive <<< file size: ', file_size)
    return file_size


def send_file(sock, file):
    print('>>> Send    >>> send file: ', file)
    sock.sendall(file)


# UTIL
def bytes_to_int(bytes_to_process):
    result = 0

    for b in bytes_to_process:
        result = result * 256 + int(b)

    return result
