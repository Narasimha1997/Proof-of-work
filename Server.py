import socket
import hashlib
from threading import Thread
import json
import uuid

class ComputeThread(Thread):

    def __init__(self, socket, text, difficulty, destination):
        self.socket = socket
        self.text = text
        self.difficulty = difficulty
        Thread.__init__(self)
        self.destination = destination
    
    def run(self):
        magic_sequence = '0'*self.difficulty
        #compute:
        while True:
            random = uuid.uuid4()
            #compute hash:
            hash_ = hashlib.sha512((self.text+str(random)).encode()).hexdigest()
            if hash_.startswith(magic_sequence) :
                data = json.dumps({
                    "hash" : hash_,
                    "signature" : str(random)
                })
                self.socket.sendto(bytes(str(data).encode()), self.destination)
                break

class Verification(Thread):

    def __init__(self, socket, uid, text, difficulty, addr):
        self.socket = socket
        self.uid = uid
        self.text = text
        self.difficutly = difficulty
        self.addr = addr
        Thread.__init__(self)
    
    def run(self):
        magic_sequence = '0'*self.difficutly
        
        if hashlib.sha512((self.text+self.uid).encode()).hexdigest().startswith(magic_sequence):
            response = {
                "success" : True,
                "identity" : "Verified"
            }
            data = json.dumps(response)
            self.socket.sendto(data.encode(), self.addr)
        else:
            response = {
                "success" : True,
                "identity" : "Not-Verified"
            }
            data = json.dumps(response)
            self.socket.sendto(data.encode(), self.addr)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(('localhost', 4555))
while True:

    data, addr = sock.recvfrom(4096)
    data = json.loads(data.decode())
    if data['operation'] == 'generate':
        ComputeThread(sock, data['text'], data['difficulty'], addr).start()
    
    elif data['operation'] == 'verify':
        Verification(sock, data['uid'], data['text'], data['difficulty'], addr).start()