import socket
import json

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = {
    "operation" : "generate",
    "text" : "Welcome to KSIT",
    "difficulty" : 3
}
data = json.dumps(data)
sock.sendto(data.encode(),('localhost', 4555))

result = sock.recv(4096).decode()

result = json.loads(result)

print(result)
#verification
data = {
    "uid" : result['signature'],
    "difficulty" : 3,
    "text" :  "Welcome to KSIT!",
    "operation" : "verify"
}
data = json.dumps(data)
sock.sendto(data.encode(), ('localhost', 4555))

result = sock.recv(4096).decode()

print(result)