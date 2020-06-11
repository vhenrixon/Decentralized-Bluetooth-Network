from bluetooth import * 
import random 
import json 
import ast
import python_jwt as jwt, jwcrypto.jwk as jwk, datetime
import uuid 
import time

class Node:

    def __init__(self, token, starting_prefix):
        # A node is a client and a server 
        self.token = token  #TODO: add verficiation of nodes
        self.socket = BluetoothSocket(RFCOMM)
        self.neighbors = [] # A list of neighbors that are nearby
        self.starting_prefix = starting_prefix
        self.server_limits = 3
        self.server_port = 3
        self.recv_limit = 2048
        self.server_address = None 
        self.connections = []
        self.client_connections = []
        self.current_topic = {}
        self.change_flag = False
        self.new_topic = {}
        self.key = jwk.JWK.generate(kty='RSA', size=2048)

    def setup(self):
        print(" -- Setting up Node -- ")
        self.setup_server()
        self.connect_to_neighbors()

    def connect_to_neighbors(self):
        # All servers should have keyboard in there name
        self.find_neighbors()
        print("Connecting to Neighbors")
        if len(self.neighbors) > 0:
            for node in self.neighbors:
                if node not in self.connections:
                    self.socket.connect((node, self.server_port))
                    self.connections.append(node)
        else:
            print("No Neighbors found")

    def find_neighbors(self):
        nearby_devices = discover_devices()
        print(" Finding Neighbors")
        for addr in nearby_devices: 
            if lookup_name(addr)[:3] == self.starting_prefix and addr not in self.neighbors:
                print("Found: "+lookup_name(addr))
                self.neighbors.append(addr)

    def setup_server(self):
        try:
            self.server_address = self.starting_prefix+"-"+str(uuid.getnode())
            self.socket.bind((self.server_address, self.server_port))
            self.socket.listen(self.server_limits)
            print("Server has been setup")        
        except BluetoothError:
            #TODO add a error 
            pass


    def _client_tick(self):
        conn, addr = self.socket.accept()
        self.client_connections.append(conn)
        previous = None
        for node in client_connections: 
            data = node.recv(recv_limit)
            header, claim = jwt.verify_jwt(data, self.key, ['PS256']) 
            if previous is None: 
                previous = claim
            else: 
                if current_topic['uuid'] != claim['uuid']:
                    self.current_topic = claim
                    # TODO: write a system that determines which to choose either the claim or the current_topic
                    
    def send_message(self, message):
        self.change_flag = True
        message_base = {"content": {message}, "uuid": uuid.uuid1()}
        self.new_topic = jwt.generate_jwt(message_base, self.key, 'PS256', datetime.timedelta(minutes=5)) 
        # TODO verfify that the message is written correctly to a standard or make a template 
        
    def tick(self): 
        self.connect_to_neighbors()
        self._client_tick()
        if self.change_flag:
            self.socket.send(str(self.new_topic))
            self.new_topic = {}
        time.sleep(10)
        self.tick() # Enters a recursive loop every ten seconds


