import math
from typing import Tuple
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

DAY = 18

'''
Your code here
Put the result in `ans` as a str or int.
'''
'''
Approach:
- Store the setup as a binary tree
    - each node represents an element
    - each node can either have two children or a regular number within the node
- Explode a pair:
    - Trigger: if pair is nested inside 4 pairs (i.e. depth=5 or 4?), the leftmost pair is targeted
    - Behaviour: traverse up the node to find the closest parent with a left child. Then add the left element to the left child.
    - Similarly for the right element
- Splitting:
    - Trigger: if a regular number is >= 10, leftmost of such element is targeted
    - Behaviour: replace element with a pair
    - left child is regular number divided by two rounded down
    - right child is regular number divided by two rounded up
- evaluate based on a LIFO approach (stack)

- magnitude:
    - recurisvely: 3*left child + 2*right child
'''
''' SnailNode should encode either regular number or a pair'''
class SnailNode:
    ''' 
    value is the value of the regular number
    value=None for pair Nodes
    '''
    def __init__(self, tree, parent, value=None) -> None:
        self.tree = tree
        self.parent = parent
        self.left = None
        self.right = None
        if value == None:
            self.type = 'pair'
        else:
            self.type = 'regular'
            self.value = value

    def explode(self):
        memory = str(self)

        if self.type == 'regular':
            raise Exception('regular numbers cannot explode')
        
        self.type = 'regular'
        self.value = 0
        l, r = self.find_leftmost_regular(), self.find_rightmost_regular()
        # if self.left.value == 6 and self.right.value == 7:
        #     print(self, self.parent,l,r)
        #     return
        left, right = self.left.value, self.right.value
        self.left, self.right = None, None

        if l != None:
            l.value += left
        if r != None:
            r.value += right
            
        print('exploded', memory, '\t|', self.tree.root)
        if l != None and l.value >= 10:
            l.split()
        if r != None and r.value >= 10:
            r.split()


    def split(self):
        memory = str(self)

        if self.type == 'pair':
            raise Exception('pairs cannot split')

        v = self.value
        self.left = SnailNode(self.tree, self, math.floor(v/2))
        self.right = SnailNode(self.tree, self, math.ceil(v/2))

        self.value = None
        self.type = 'pair'
        print('splited', memory, '\t\t|', self.tree.root)

        visiting = self
        depth = 1
        while visiting.parent != None:
            visiting = visiting.parent
            depth += 1

        if depth > 4:
            self.explode()


    def find_leftmost_regular(self):
        prev = self
        visiting = self.parent
        while visiting is not None:
            if visiting.left != prev:
                if visiting.left.type == 'regular':
                    return visiting.left
                
                visiting = visiting.left
                while visiting.type != 'regular':
                    visiting = visiting.right
                return visiting
            
            else:
                prev = visiting
                visiting = visiting.parent

        return None
        
    def find_rightmost_regular(self):
        prev = self
        visiting = self.parent
        while visiting is not None:
            if visiting.right != prev:
                if visiting.right.type == 'regular':
                    return visiting.right
                
                visiting = visiting.right
                while visiting.type != 'regular':
                    visiting = visiting.left
                return visiting
            
            else:
                prev = visiting
                visiting = visiting.parent
        
        return None

    def get_magnitude(self):
        if self.type == 'pair':
            return self.left.get_magnitude()*3 + self.right.get_magnitude()*2
        else:
            return self.value

    def __repr__(self) -> str:
        if self.type == 'pair':
            return f'[{self.left}, {self.right}]'
        else:
            return f'{self.value}'

def parse_s(tree, s):
    root = None
    visiting = None
    buffers = []
    for c in s:
        match c:
            case '[':
                node = SnailNode(tree, visiting)
                if visiting == None:
                    root = node
                else:
                    buffers[-1].append(node)
                visiting = node
                buffers.append([])

            case ']':
                buffer = buffers.pop()
                if isinstance(buffer[0], str):
                    visiting.right = SnailNode(tree, visiting, int(''.join(buffer)))
                else:
                    visiting.right = buffer[0]
                visiting = visiting.parent

            case ',':
                buffer = buffers[-1]
                if isinstance(buffer[0], str):
                    visiting.left = SnailNode(tree, visiting, int(''.join(buffer)))
                else:
                    visiting.left = buffer[0]
                buffers[-1] = []

            case _:
                buffers[-1].append(c)

    return root


class SnailTree:
    def __init__(self, s) -> None:
        self.root = parse_s(self, s)
        
    def __iadd__(self, other):
        left = self.root
        right = other.root
        self.root = SnailNode(self, None)

        left.parent = self.root
        right.parent = self.root

        self.root.left = left
        self.root.right = right

        self.update_trees()

        self.reduce()
        print('\tres', self.root)
        return self
    
    def update_trees(self):
        stack = [self.root]
        while len(stack) > 0:
            node = stack.pop()
            node.tree = self
            if node == 'pair':
                stack.append(node.left)
                stack.append(node.right)


    def reduce(self):
        # node = self.root.left.right.right.left
        # node.explode()
        # print(node)

        # traversal
        stack = [(self.root,1)]
        node = self.root
        curr_depth = 1
        
        while True:
            if node != None and len(stack) > 0:
                stack.append((node, curr_depth))
                node = node.left
                curr_depth += 1

            elif len(stack) > 0:
                node, depth = stack.pop()
                curr_depth = depth

                # validation
                if node.type == 'pair' and depth > 4:
                    node.explode()
                if node.type == 'regular' and node.value >= 10:
                    node.split()

                node = node.right
                curr_depth += 1

            else:
                break


    def get_magnitude(self):
        return self.root.get_magnitude()

def func1(s):
    tree = None
    for line in s.split('\n'):
        if tree == None:
            tree = SnailTree(line)
        else:
            tree += SnailTree(line)

    return tree.get_magnitude()

# s = get_example(DAY).strip() # the daily input is stored in s
s = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''
s = '''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]'''
s = '''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]'''
# s = '''[[[[4,3],4],4],[7,[[8,4],9]]]
# [1,1]'''
# print(s)
# s = get_input(DAY).strip() # the daily input is stored in s

ans1 = func1(s)
submit(DAY, 1, ans1)
# s = '[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]'
# tree = SnailTree(s)
# tree.reduce()
# print(tree.root)
# tree = SnailTree('[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]')
# print(tree.get_magnitude())

# def func2(s):
#     pass
# ans2 = func2(s)

# submit(DAY, 2, ans2)