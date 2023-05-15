from src.node import Node

class Stack :
  def __init__(self,data):
    self.last_node = Node(data)
    self.size = 1

  def push(self,data):
    N = Node(data)
    N.next_node = self.last_node
    self.lest_node = N
    self.size += 1

  def pop(self):
    data = self.last_node.data
    self.last_node = self.last_node.next_node
    self.size -= 1
    return data

  def size(self):
    return self.size

  def peek(self):
    return self.last_node.data