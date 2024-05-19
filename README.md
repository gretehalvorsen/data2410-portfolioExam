# DATA2410 Reliable Transport Protocol (DRTP)

In this project, my aim was to design and develop the DATA2410 Reliable Transport Protocol (DRTP) - a simple reliable data transfer protocol, built upon UDP. It is specifically engineered to guarantee reliable data delivery in the correct sequence, eliminating any instances of missing or duplicate data.

The result is an executable file transfer application, application.py. This application is programmed to use command-line arguments to trigger a client and server. The client's role is to read a jpeg file from the system and dispatch it via DRTP/UDP. The filename, server address, and port number are all provided as command-line arguments. Additionally, you have the option to define a preferred window size for file transfer.

## How to Run

1. Open a terminal.
2. Navigate to the directory where `application.py` is located.
3. To start the server with default values, use the command: <br>
`python3 application.py -s -i your_ip -p your_port`. <br>
Replace `your_ip` and `your_port` with your desired IP address and port number.
To run with default values ip: 10.0.1.2 and port: 8088 use command: <br>
`python3 application.py -s` <br>
4. To start the client, use the command: <br>
`python3 application.py -c -i server_ip -p server_port` <br>
Or run with default values: `python3 application.py -c`

## Command Line Arguments

The following arguments are available for configuration:

| Flag | Long Flag | Input | Type | Description |
| ---- | --------- | ----- | ---- | ----------- |
| -s   | --server  | X     | boolean | Enable the server mode |
| -c   | --client  | X     | boolean | Enable the client mode |
| -i   | --ip      | IP address | string | Allows to bind the IP address at the server side. The client will use this flag to select server's IP for the connection - It must be in the dotted decimal notation format, default: 10.0.1.2 |
| -p   | --port    | Port number | integer | Allows to use select port number on which the server should listen and at the client side, it allows to select the server's port number; the port must be an integer and in the range [1024, 65535], default: 8088 |
| -f   | --file    | X | string | Allows you to name the received file on server side and choose the file to tranfser from client side |
| -w   | --window  | X | int | Sliding window size, default: 3. Can only be set for client|
| -d   | --discard | X | int | A custom test case to skip a seq to check for retransmission. If you pass -d 11 on the server side, your server will discard packet with seq number 11 only for once. Can only be set for server

## Sources

The foundation for my code is based on previous assignments, lab exercises, as well as sample code provided on [github - DATA2410](https://github.com/safiqul/2410), and within "Computer Networking: A Top-Down Approach." I also used Sikt KI-chat as a tool for identifying and resolving bugs in the code.


At the start of the assignment, I drew inspiration for my own work from code provided by one of the [Teaching Assistants](https://github.com/HamidHamrah/DRTP). However, the GitHub repository containing this code has since been set to private. 

