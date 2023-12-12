from dataclasses import dataclass
from typing import Any, List


@dataclass
class Node:
    value: Any
    next: 'Node' 
    
    
@dataclass
class LastNodeDetails:
    length: int
    last: Node


class LinkedList:
    head: Node
    
    def __init__(self, head: Node = None) -> None:
        self.head = head
        
    def delete_node(self, node: Node) -> None:
        if not node or not node.next:
            node = None    
        else:
            node.value = node.next.value
            node.next = node.next.next
            
    def remove_first(self) -> Node:
        if not self.head:
            return None
        
        node = self.head
        self.head = self.head.next
        return node
        
    def remove_last(self) -> Node:
        if not self.head or not self.head.next:
            self.head = None
            
        current = self.head
        while current and current.next.next:
            current = current.next
        
        node = current.next
        current.next = None
        return node
        
    def insert_first(self, node: Node) -> None:
        node.next = self.head
        self.head = node
        
    def insert_last(self, node: Node) -> None:
        if not self.head:
            self.head = node
        
        current = self.head
        while current and current.next:
            current = current.next
            
        current.next = node
    
    def to_list(self) -> List[int]:
        numbers = []
        if not self.head:
            return numbers
        
        current = self.head
        while current:
            numbers.append(current.value)
            current = current.next
            
        return numbers
    
    def clone(self) -> 'LinkedList':
        cloned_head=Node(value=self.head.value, next=None)
        
        cloned = cloned_head
        current = self.head.next
        while current:
            node = Node(value=current.value, next=None)
            cloned.next = node
            cloned = node
            current = current.next
            
        return LinkedList(head=cloned_head)
    