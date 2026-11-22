import random

with open("jokes.txt", encoding="utf-8") as f:
    JOKES = f.read().splitlines()

Loglist = []

class Node:
    def __init__(self, nodeid: int, total_nodes: int):
        self.lamport_timestamp = 0
        self.vector_timestamp = [0] * total_nodes
        self.id = nodeid

    def GenerateMsg(self):
        return random.choice(JOKES)

    def Log(self, msg):
        Loglist.append([self.id, self.lamport_timestamp, tuple(self.vector_timestamp), msg])
        
    def Send(self, recv_node):
        self.lamport_timestamp += 1
        self.vector_timestamp[self.id] += 1
        msg = self.GenerateMsg()
        self.Log(f"sent: {msg}")
        recv_node.Receive(self.lamport_timestamp, self.vector_timestamp, msg)

    def Receive(self, new_lamport, new_vector, msg):
        self.lamport_timestamp = max(new_lamport, self.lamport_timestamp) + 1
        self.vector_timestamp = [max(v1, v2) for v1, v2 in zip(self.vector_timestamp, new_vector)]
        self.vector_timestamp[self.id] += 1
        self.Log(f"recv: {msg}")

    def Event(self):
        self.lamport_timestamp += 1
        self.vector_timestamp[self.id] += 1
        self.Log(self.GenerateMsg())
        
def simulation(N, steps, send_probability, seed):
    random.seed(seed)
    Loglist.clear()
    Nodes = []
    for n in range(N):
        Nodes.append(Node(n, N))

    for step in range(steps):
        sender = random.choice(Nodes)
        if random.random() < send_probability:
            others = []
            for n in Nodes:
                if n is not sender:
                    others.append(n)
            receiver = random.choice(others)
            sender.Send(receiver)
        else:
            sender.Event()

    return list(Loglist)

    
