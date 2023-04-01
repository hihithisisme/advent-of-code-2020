from collections import Counter
from typing import List
from utils import get_aoc_token 

import requests

AOC_COOKIE = get_aoc_token()
YEAR = '2021'

def get_input(day):
    req = requests.get(f'https://adventofcode.com/{YEAR}/day/{day}/input', 
                       headers={'cookie':'session='+AOC_COOKIE})
    return req.text

def get_example(day,offset=0):
    req = requests.get(f'https://adventofcode.com/{YEAR}/day/{day}',
                       headers={'cookie':'session='+AOC_COOKIE})
    return req.text.split('<pre><code>')[offset+1].split('</code></pre>')[0]

def submit(day, level, answer):
    print(f'You are about to submit the follwing answer:')
    print(f'>>>>>>>>>>>>>>>>> {answer}')
    input('Press enter to continue or Ctrl+C to abort.')
    data = {
      'level': str(level),
      'answer': str(answer)
    }

    response = requests.post(f'https://adventofcode.com/{YEAR}/day/{day}/answer',
                             headers={'cookie':'session='+AOC_COOKIE}, data=data)
    if 'You gave an answer too recently' in response.text:
        # You will get this if you submitted a wrong answer less than 60s ago.
        print('VERDICT : TOO MANY REQUESTS')
    elif 'not the right answer' in response.text:
        if 'too low' in response.text:
            print('VERDICT : WRONG (TOO LOW)')
        elif 'too high' in response.text:
            print('VERDICT : WRONG (TOO HIGH)')
        else:
            print('VERDICT : WRONG (UNKNOWN)')
    elif 'seem to be solving the right level.' in response.text:
        # You will get this if you submit on a level you already solved.
        # Usually happens when you forget to switch from `PART = 1` to `PART = 2`
        print('VERDICT : ALREADY SOLVED')
    else:
        print('VERDICT : OK !')

DAY = 12
# s = get_example(DAY).strip() # the daily input is stored in s
# print(s)
s = get_input(DAY).strip() # the daily input is stored in s

'''
Your code here
Put the result in `ans` as a str or int.
'''
class Node:
    def __init__(self, id: str):
        self.id = id
        self.nei = set()

    def add_nei(self, nei):
        self.nei.add(nei)

    def get_nei(self):
        return self.nei
    
    def is_small_cave(self):
        return self.id.islower()
    
    def __repr__(self) -> str:
        return f'Node {self.id}'


class Solution:
    def __init__(self, s, allow_special_cave):
        self.nodes = {}
        self.allow_special_cave = allow_special_cave
        for line in s.split('\n'):
            node1, node2 = line.split('-')

            if node1 not in self.nodes:
                self.add_node(node1)
            if node2 not in self.nodes:
                self.add_node(node2)

            self.nodes[node1].add_nei(self.nodes[node2])
            self.nodes[node2].add_nei(self.nodes[node1])

    def add_node(self, node_id):
        node = Node(node_id)
        self.nodes[node_id] = node

    def dfs(self, node, explored_orig, cpath, special_cave = None):
        path = [p for p in cpath]
        explored = explored_orig.copy()
        
        if node.id == 'end':
            path.append(node.id)
            # print(path)
            return 1
        
        sc = special_cave
        if node.is_small_cave():
            if node in explored and special_cave == None:
                sc = node
            elif node in explored and special_cave != None:
                raise Exception('how can this be??!?!?!!')
            else:
                explored.add(node)
            
        path.append(node.id)
        total = 0
        
        for nei in node.get_nei():
            if nei.is_small_cave():
                if nei.id == 'start':
                    continue
                if nei in explored:
                    if not self.allow_special_cave:
                        continue
                    elif self.allow_special_cave and sc != None:
                        continue
                    
            
            total += self.dfs(nei, explored, path, sc)

        return total
        


def func1(s):
    sol = Solution(s, False)
    
    return sol.dfs(sol.nodes['start'], set())

# ans1 = func1(s)

# submit(DAY, 1, ans1)

def func2(s):
    sol = Solution(s, True)
    return sol.dfs(sol.nodes['start'], set(), [])
ans2 = func2(s)

submit(DAY, 2, ans2)