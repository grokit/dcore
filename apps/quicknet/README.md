
# Quicknet

quicknet: do simple 'net' (TCP, HTTP, HTTPS, ...) operations from the commands line for both the sending and receiving flows.
          
Meant as a simple tool to hack things together when you want to leverage python's libs.
For one liners you might want to take a look at 'curl' as well.

# Example(s)

Send a test TCP packet to localhost port 500:

    quicknet -m tcp -t localhost:500 -p Test payload.
