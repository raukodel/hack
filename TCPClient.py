import socket
import sys

from TCPUtil import *

print(sys.version)


# LOOP
def connect():
    # Connect the socket to the port where the server is listening
    server_address = ('172.16.201.35', 112)

    try:
        sock.connect(server_address)

        option = ""
        while option != 'exit':
            option = input("Enter option [1 - Write file] [2 - Receive file] [3 - Run command] [Exit]: ")  # take input
            option = option.lower().strip()

            # WRITE
            if option == '1':
                file_name = input("File name: ")  # take input
                file_content = check_if_file_exist(file_name)

                if file_content is not None:
                    send_status(sock, ConnectionType.WRITE)

                    if receive_status(sock) == ConnectionType.SERVER_OK.value:
                        packed = get_packed(file_content)
                        send_size(sock, packed)

                        if receive_status(sock) == ConnectionType.SERVER_OK.value:
                            send_file(sock, packed)

            # RECEIVE
            elif option == '2':
                send_status(sock, ConnectionType.SEND)

                if receive_status(sock) == ConnectionType.SERVER_OK.value:
                    run_receive_file()

            # COMMAND
            elif option == '3':
                run_command()

    except socket.error as exc:
        print("Caught exception socket.error : %s" % exc)
        send_status(sock, ConnectionType.END_CONNECTION)

        close_connection()

    finally:
        send_status(sock, ConnectionType.END_CONNECTION)

        close_connection()


# RECEIVE FILE
def run_receive_file():
    file_size = sock.recv(1024)

    if file_size is not None:
        file_size = struct.unpack("H", file_size)[0]

        packed_data = sock.recv(file_size)
        file_data = FileTupleData(*struct.unpack(str(file_size) + "s", packed_data))
        print('<<< Receive <<< file: ', file_data.data)

        file = open('data_server.json', 'wb+')
        file.write(file_data.data)
        file.close()


# RUN COMMAND
def run_command():
    command = input("Enter command: ")  # take input

    while command.lower().strip() != 'exit':
        send_status(sock, ConnectionType.COMMAND)

        if receive_status(sock) == ConnectionType.SERVER_OK.value:
            # Send command to the server
            command = command.encode('utf-8')
            print('>>> Send    >>> run command: ', command)
            sock.sendall(command)

            # Receive the output of that command
            output = sock.recv(1024)
            output = output.decode('ISO-8859-1')
            print('<<< Receive <<< data from server: ', output)

            command = input("Enter command: ")  # again take input
        else:
            print('!!!!!!!!!')
            break


# CONNECTION
def close_connection():
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()


# MAIN
def main():
    # Create a TCP/IP socket
    try:
        global sock
        global FileTupleData

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        FileTupleData = collections.namedtuple("FileData", "data")
    except socket.error:
        print("Failed to create socket")
        sys.exit(1)

    connect()


# if __name__ == "__main__":
main()
