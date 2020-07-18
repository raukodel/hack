import socket
import sys
import threading
import subprocess
import shlex

from TCPUtil import *


def start_server():
    print('---------- Listening ----------')
    print('waiting for a connection')

    while True:
        # Wait for a connection
        connection, client_address = sock.accept()
    
        # spin off a thread to handle our new client
        client_thread = threading.Thread(target=client_handler, args=(connection, client_address))
        client_thread.start()        


# LOOP
def client_handler(connection, client_address):
    try:
        print('connection from', client_address)
    
        # Receive the data in small chunks and retransmit it
        while True:
            # Receive type option
            client_request = struct.unpack("H",  connection.recv(1024))[0]
            print('<<< Receive <<< receive request: ', ConnectionType(client_request))
             
            # receive file
            if client_request == ConnectionType.WRITE.value:
                send_status(connection, ConnectionType.SERVER_OK)
    
                file_size = receive_file_size(connection)
                
                send_status(connection, ConnectionType.SERVER_OK)
                
                receive_file(connection, file_size)
                
                send_status(connection, ConnectionType.SERVER_OK)

            # Send file
            if client_request == ConnectionType.SEND.value:
                send_status(connection, ConnectionType.SERVER_OK)

                file_content = check_if_file_exist("data.json")
                packed = get_packed(file_content)
                send_size(connection, packed)
                send_file(connection, packed)

            # Run command
            if client_request == ConnectionType.COMMAND.value:
                send_status(connection, ConnectionType.SERVER_OK)

                run_command(connection)

            # End connection handler
            if client_request == ConnectionType.END_CONNECTION.value:
                send_status(connection, ConnectionType.SERVER_OK)
                print('no more data from', client_address)
                print('---------- End ----------')
                print('waiting for a connection')
                break

    except socket.error as exc:
        print("Caught exception socket.error : %s" % exc)
    
    finally:
        connection.close()


# RECEIVE FILE
def receive_file(connection, file_size):
    packed_data = connection.recv(file_size)
    file_data = FileTupleData(*struct.unpack(str(file_size) + "s", packed_data))
    print('<<< Receive <<< file: ', file_data.data)

    file = open('file.py', 'wb+')
    file.write(file_data.data)
    file.close()


# RUN COMMAND
def run_command(connection):
    command = connection.recv(1024)
    command = command.decode('utf-8')
    command = shlex.split(command)
    print('<<< Receive <<< command: ', command)

    try:
        # Run the command and retrieve its output
        output = "Output: ".encode('utf-8')
        output += subprocess.check_output(command, shell=True)
        print('>>> Send    >>> server command output: ', output)
        connection.sendall(output)
    except subprocess.CalledProcessError:
        output = "Failed to execute command."
        connection.sendall(output.encode('utf-8'))


# MAIN
def main():
    global sock
    global FileTupleData

    print(sys.version)

    FileTupleData = collections.namedtuple("FileData", "data")

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('172.16.201.35', 112)
    print(sys.stderr, 'starting up on %s port %s' % server_address)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    start_server()


main()
