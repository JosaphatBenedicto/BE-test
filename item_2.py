"""
Item 2.
 Create a simple application that rewrites the json data structure using 
 Section A to Section B. Please note that Section A nodes are sorted in 
 no particular order. The "subordinate" node must be removed when no 
 child exists (see markcorderoi and richard)
"""
import json
from typing import Dict, Any, List

def add_sibling():
    return

def add_subordinate():
    return

def find_name(name:str, ):
    return

"""
case 1. 
    New entry, no manager_name and no login_name match
action:
    add new branch

case 2.
    manager_name match but no login_name match
action:
    add login_name as subordinate to matched manager_name

case 3.
    login_name match but no manager_name match
action:
    rewrite the branch with the matched login_name as manager_name

case 4.
    manager_name and login_name match
action:
    add entire branch of login_name as subordinate to matched manager_name

functions:
    - find_name
        - returns the branch with the matched name
    - add_sibling
        - add new dictionary to the list
    - add_subordinate
        - if no subordinate exists, add the new one
        - if subordinate exists, add the new one as a dictionary to the list
    - add_name
        - add the branch as a subordinate to the matched manager_name
"""

class Node():
    def __init__(self, name: str):
        self.name = name
        self.subordinate = None
        self.sibling = None

    def update(self, node: 'Node'):
        self = node

    def update_subordinate(self, subordinate: 'Node'):
        print("Updating subordinate for node:", self.name)
        if self.subordinate is None:
            self.subordinate = subordinate
            print("Subordinate added as first child.")
        else:
            print("Subordinate already exists, appending to siblings.")
            self.append_subordinate(subordinate)

    def append_subordinate(self, subordinate: 'Node'):
        print("Appending subordinate to node:", self.name)
        current = self.subordinate
        while current.sibling is not None:
            current = current.sibling
        current.sibling = subordinate
        print("Subordinate appended as sibling:", subordinate.name)

    def find_node(self, name: str) -> 'Node':
        print("Finding node with name:", name)
        if self.name == name:
            return self
        if self.subordinate != None:
            print("Searching in subordinate:", self.subordinate.name)
        if self.sibling != None:
            return self.sibling.find_node(name)
        return None
    
    def __repr__(self):
        return f"Node(name={self.name}, subordinate={self.subordinate}, sibling={self.sibling})"

def main():
    with open('./section_a.json', 'r') as file:
        section_a_data = json.load(file)

    with open('./section_b.json', 'r') as file:
        section_b_data = json.load(file)

    section_b = []

    for entry in section_a_data:
        print("\nProcessing entry:", entry)

        for current in section_b:
            print("Current node in section B:", current)
            manager_node = current.find_node(entry['manager_name'])
            print("Manager node:", manager_node)
            login_node = current.find_node(entry['login_name'])
            print("Login node:", login_node)
            if manager_node is None and login_node is not None:
                new_node = Node(entry['manager_name'])
                new_node.update_subordinate(login_node)
                print("Creating new node for manager:", new_node)
                current.update(new_node)
                print("Adding node as subordinate to login node:", current)
            elif manager_node is not None and login_node is None:
                print("Found manager node:", manager_node)
                manager_node.add_subordinate(Node(entry['login_name']))
                print("Adding login node as subordinate to manager node:", manager_node)
            else:
                print("No match found, adding new node.")
                section_b.append(node)
                break

        if section_b==[]:
            node = Node(name=entry['manager_name'])
            node.update_subordinate(Node(name=entry['login_name']))
            print("Section B is empty, adding new node.")
            section_b.append(node)

        print("Updated section B:", section_b)

    # print(json.dumps(section_b_data, indent=4))



if __name__ == "__main__":
    main()