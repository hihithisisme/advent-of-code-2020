import copy
import heapq
from time import time
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

DAY = 15
# s = get_example(DAY).strip() # the daily input is stored in s
# s = """116
# 138
# 213"""
# s = """19999
# 19111
# 11191"""
# print(s)
s = get_input(DAY).strip() # the daily input is stored in s

'''
Your code here
Put the result in `ans` as a str or int.
'''

class Node:
    def __init__(self, x, y, weight) -> None:
        self.x = x
        self.y = y
        self.weight = weight

    def __eq__(self, other) -> bool:
        return self.weight == other.weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __repr__(self) -> str:
        return str((self.x, self.y, self.weight))

"""
Lessons learnt:
- for dijkstra, we are always processing the next nearest node to the origin
    - therefore, while adding neighbours into the heap, if it is the first time that we see the neighbours, it should be the shortest path to the neighbour as well
    - hence we can add to the memo when we add neighbours
"""
class Solution_dijkstra:
    def __init__(self, s, part2 = False):
        self.arr = []
        for line in s.split('\n'):
            nums = [int(n) for n in line]
            if part2:
                row_template = nums.copy()
                for i in range(1,5):
                    nums += [wrap_incr(n, i) for n in row_template]
            self.arr.append(nums)

        if part2:
            col_template = copy.deepcopy(self.arr)
            for i in range(1,5):
                for row in col_template:
                    self.arr.append([wrap_incr(n, i) for n in row])

        self.ROWS = len(self.arr)
        self.COLS = len(self.arr[0])
        self.explored = {}
        self.heap = [Node(0,0,0)]

    def add_neighbours(self, x, y):
        for xi in range(-1, 2, 2):
            if xi + x < self.ROWS and xi + x >= 0:
                n = Node(xi + x, y, self.arr[xi + x][y] + self.explored[(x,y)])
                pos = (n.x, n.y)
                if pos not in self.explored:
                    self.explored[pos] = n.weight
                    heapq.heappush(self.heap, n)

        for yi in range(-1, 2, 2):
            if yi + y < self.COLS and yi + y >= 0:
                n = Node(x, yi + y, self.arr[x][yi + y] + self.explored[(x,y)])
                pos = (n.x, n.y)
                if pos not in self.explored:
                    self.explored[pos] = n.weight
                    heapq.heappush(self.heap, n)


    def dijkstra(self):
        count = self.ROWS * self.COLS
        while len(self.heap) > 0:
            count -= 1
            node = heapq.heappop(self.heap)
            pos = (node.x, node.y)

            if pos == (0,0):
                self.explored[(node.x, node.y)] = 0

            if pos == (self.ROWS - 1, self.COLS - 1):
                # lines = []
                # for i in range(self.ROWS):
                #     arr = []
                #     for j in range(self.COLS):
                #         if (i,j) in self.explored:
                #             arr.append(str(self.explored[(i,j)]))
                #         else:
                #             arr.append('#')
                #     line = '\t'.join(arr)
                #     lines.append(line)
                # print('\n'.join(lines))
                return self.explored[pos]
            
            self.add_neighbours(node.x, node.y)

            if count <= 0:
                break
            
        raise Exception('no path to the bottom right????!?!?!?!')

class AStar_Node:
    def __init__(self, x, y, dist, des) -> None:
        self.x = x
        self.y = y
        self.dist = dist
        self.des = des

    # def __eq__(self, other) -> bool:
    #     return self.weight == other.weight

    def __lt__(self, other):
        return self.get_weight() < other.get_weight()

    def __repr__(self) -> str:
        return str((self.x, self.y, self.weight))
    
    def get_hereustic(self):
        return self.des[0] - self.x + (self.des[1] - self.y)
    
    def get_weight(self):
        return self.dist + self.get_hereustic()

def wrap_incr(n, i):
    return (n-1 + i) % 9 + 1

class Solution_astar:
    def __init__(self, s, part2=False):
        self.arr = []
        for line in s.split('\n'):
            nums = [int(n) for n in line]
            if part2:
                row_template = nums.copy()
                for i in range(1,5):
                    nums += [wrap_incr(n, i) for n in row_template]
            self.arr.append(nums)

        if part2:
            col_template = copy.deepcopy(self.arr)
            for i in range(1,5):
                for row in col_template:
                    self.arr.append([wrap_incr(n, i) for n in row])

        self.ROWS = len(self.arr)
        self.COLS = len(self.arr[0])
        self.explored = {}
        self.heap = [Node(0,0,0)]

    

    def add_neighbours(self, x, y):
        for xi in range(-1, 2, 2):
            if xi + x < self.ROWS and xi + x >= 0:
                n = AStar_Node(xi + x, y, self.arr[xi + x][y] + self.explored[(x,y)], (self.ROWS-1, self.COLS-1))
                pos = (n.x, n.y)
                if pos not in self.explored:
                    self.explored[pos] = n.dist
                    heapq.heappush(self.heap, n)

        for yi in range(-1, 2, 2):
            if yi + y < self.COLS and yi + y >= 0:
                n = AStar_Node(x, yi + y, self.arr[x][yi + y] + self.explored[(x,y)], (self.ROWS-1, self.COLS-1))
                pos = (n.x, n.y)
                if pos not in self.explored:
                    self.explored[pos] = n.dist
                    heapq.heappush(self.heap, n)


    def astar(self):
        count = self.ROWS * self.COLS
        while len(self.heap) > 0:
            count -= 1
            node = heapq.heappop(self.heap)
            pos = (node.x, node.y)

            if pos == (0,0):
                self.explored[(node.x, node.y)] = 0

            if pos == (self.ROWS - 1, self.COLS - 1):
                # lines = []
                # for i in range(self.ROWS):
                #     arr = []
                #     for j in range(self.COLS):
                #         if (i,j) in self.explored:
                #             arr.append(str(self.explored[(i,j)]))
                #         else:
                #             arr.append('#')
                #     line = '\t'.join(arr)
                #     lines.append(line)
                # print('\n'.join(lines))
                return self.explored[pos]
            
            self.add_neighbours(node.x, node.y)

            if count <= 0:
                break
            
        raise Exception('no path to the bottom right????!?!?!?!')


def func1(s):
    start = time()
    sol = Solution_dijkstra(s).dijkstra()
    print(time() - start)
    
    start = time()
    sol = Solution_astar(s).astar()
    print(time() - start)
    return sol

# ans1 = func1(s)

# submit(DAY, 1, ans1)

def func2(s):
    # somehow AStar algo is off by a few 
    # sol = Solution_astar(s, True).astar()
    sol = Solution_dijkstra(s, True).dijkstra()
    return sol

ans2 = func2(s)

submit(DAY, 2, ans2)