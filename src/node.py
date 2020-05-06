from bluetooth import * 
import random 
import json 
import ast

class Node:

    def __init__(self, token, starting_prefix):
        # A node is a client and a server 
        self.token = token 
        self.socket = BluetoothSocket(RFCOMM)
        self.neighbors = [] # A list of neighbors that are nearby
        self.starting_prefix = if starting_prefix !=  3: "VVV"
        self.server_limits = 3
        self.server_port = 3
        self.recv_limit = 1024
        self.server_address = None 
        self.connections = []
        self.current_topic = {}
        self.change_flag = False
        self.new_topic = {}

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
            self.socket.bind((self.start_prefix+self.create_number_series(), self.server_port))
            self.socket.listen(self.server_limits)        
        except BluetoothError:
            #TODO add a error 
            pass

    def create_number_series(self):
        rs = ""
        for i in range(30):
            rs = rs + str(i)
        return rs

    def _client_tick(self):
        conn, addr = self.socket.accept()
        self.connections.append(conn)
        # TODO: add verification via token     
        previous = None
        for node in connections: 
            data = node.recv(recv_limit)
            cleaned_data = ast.literal_eval(data) 
            if previous is None: 
                previous = cleaned_data
                self.current_topic = cleaned_data
            else: 
                if previous['signature'] != cleaned_data['signature']:
                    self.current_topic = cleaned_data
            
    def send_message(self, message):
        self.change_flag = True
        # TODO verfify that the message is written correctly to a standard or make a template 
        # sigature system 

    def tick(self): 
        self._client_tick()
        if self.change_flag:
            self.socket.send(self.new_topic)
            



