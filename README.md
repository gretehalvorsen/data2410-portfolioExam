# data2410-portfolioExam
Repository for portofolio exam in DATA2400 - Networking and cloud computing

# Command Line Arguments

The following arguments are available for configuration:

| Flag | Long Flag | Input | Type | Description |
| ---- | --------- | ----- | ---- | ----------- |
| -s   | --server  | X     | boolean | Enable the server mode |
| -c   | --client  | X     | boolean | Enable the client mode |
| -i   | --ip      | IP address | string | Allows to bind the IP address at the server side. The client will use this flag to select server's IP for the connection - use a default value if it's not provided. It must be in the dotted decimal notation format, e.g. 10.0.1.2 |
| -p   | --port    | Port number | integer | Allows to use select port number on which the server should listen and at the client side, it allows to select the server's port number; the port must be an integer and in the range [1024, 65535], default: 8088 |
| -f   | --file    | X | string | Allows you to choose the jpg file |
| -w   | --window  | X | int | Sliding window size, default: 3 |
| -d   | --discard | X | int | A custom test case to skip a seq to check for retransmission. If you pass -d 11 on the server side, your server will discard packet with seq number 11 only for once. Make sure you change the value to an infinitely large number after your first check in order to avoid skipping seq=11 all the time. |
