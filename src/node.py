from bluetooth import * 
import random 
import json 
import ast
import python_jwt as jwt, jwcrypto.jwk as jwk, datetime
import uuid 


class Node:

    def __init__(self, token, starting_prefix):
        # A node is a client and a server 
        self.token = token  #TODO: add verficiation of nodes
        self.socket = BluetoothSocket(RFCOMM)
        self.neighbors = [] # A list of neighbors that are nearby
        self.starting_prefix = if starting_prefix !=  3: "VVV"
        self.server_limits = 3
        self.server_port = 3
        self.recv_limit = 2048
        self.server_address = None 
        self.connections = []
        self.current_topic = {}
        self.change_flag = False
        self.new_topic = {}
        self.key = jwk.JWK.generate(kty='RSA', size=2048)

    def connect_to_neighbors(self):
        # All servers should have keyboard in there name
        for node in neighbors:
            self.socket.connect((node, self.server_port))

    def find_neighbors(self):
        nearby_devices = discover_devices()
        for addr in nearby_devices: 
            if lookup_name(addr)[:3] == self.starting_prefix:
                self.neighbors.append(addr)

    def setup_server(self):
        try:
            self.server_address = self.start_prefix+"-"+uuid.getnode()
            self.socket.bind((self.server_address, self.server_port))
            self.socket.listen(self.server_limits)        
        except BluetoothError:
            #TODO add a error 
            pass


    def _client_tick(self):
        conn, addr = self.socket.accept()
        self.connections.append(conn)
        previous = None
        for node in connections: 
            data = node.recv(recv_limit)
            header, claim = jwt.verify_jwt(data, self.key, ['PS256']) 
            if previous is None: 
                previous = claim
            else: 
                if current_topic['uuid'] != claim['uuid']:
                    self.currrent_topic = claim
                    # TODO: write a system that determines which to choose either the claim or the current_topic
                    
    def send_message(self, message):
        self.change_flag = True
        message_base = {"content": {message}, "uuid": uuid.uuid1()}
        self.new_topic = jwt.generate_jwt(message_base, self.key, 'PS256', datetime.timedelta(minutes=5)) 
        # TODO verfify that the message is written correctly to a standard or make a template 
        
    def tick(self): 
        self._client_tick()
        if self.change_flag:
            self.socket.send(str(self.new_topic))
            self.new_topic = {}

    '''
    Comeback because you would need to ask each node for this info 
    def node_list(self):
        print("| Node name | connection status | Server Port |")
        print("-----------------------------------------------")
        print("|"+self.server_address+"|"+"Current NODE |"+self.server_port+"|")
        for nodes in self.connection:
            print("|"+nodes.+)
     '''   

