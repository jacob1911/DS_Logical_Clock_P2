import random

Loglist = []

class Node:
    def __init__(self, nodeid: int, total_nodes: int):
        self.lamport_timestamp = 0
        self.vector_timestamp = [0] * total_nodes
        self.id = nodeid

    def GenerateMsg(self):
        return random.choice(open("jokes.txt", "r").readline().split())

    def Log(self, msg):
        Loglist.append([self.lamport_timestamp, self.vector_timestamp, msg])
        
    def Send(self, recv_node):
        self.lamport_timestamp += 1
        self.vector_timestamp[self.id] += 1
        msg = self.GenerateMsg()
        recv_node.Receive(self.lamport_timestamp, self.vector_timestamp, msg)
        self.Log(f"sent: {msg}")

    def Receive(self, new_lamport, new_vector, msg):
        self.lamport_timestamp = max(new_lamport, self.lamport_timestamp) + 1
        self.vector_timestamp = [max(v1, v2) for v1, v2 in zip(self.vector_timestamp, new_vector)]
        self.vector_timestamp[self.id] += 1
        self.Log(f"recv: {msg}")

    def Event(self):
        self.lamport_timestamp += 1
        self.vector_timestamp[self.id] += 1
        self.Log(self.GenerateMsg())
        



        
