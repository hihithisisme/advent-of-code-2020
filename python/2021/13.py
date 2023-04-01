import re
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

DAY = 13
# s = get_example(DAY).strip() # the daily input is stored in s
s = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
# print(s)
s = get_input(DAY).strip() # the daily input is stored in s

'''
Your code here
Put the result in `ans` as a str or int.
'''

class Paper:
    def __init__(self, s):
        self.dots = set()
        self.instructions = []
        for line in s.split('\n'):
            if line == "": continue
            match = re.search('fold along ([xy])\=(\d+)', line)
            if match != None:
                m = (match.group(1), int(match.group(2)))
                self.instructions.append(m)
                continue
            x, y = list(map(int, line.split(',')))
            self.dots.add((x,y))

    def fold_x(self, x):
        cp = self.dots.copy()
        for dot in cp:
            if dot[0] > x:
                diff = dot[0] - x
                self.dots.remove(dot)
                self.dots.add((dot[0] - diff * 2, dot[1]))

    def fold_y(self, y):
        cp = self.dots.copy()
        for dot in cp:
            if dot[1] > y:
                diff = dot[1] - y
                self.dots.remove(dot)
                self.dots.add((dot[0], dot[1] - diff * 2))

    def fold(self, limit = -1):
        i = 0
        for instr in self.instructions:
            if limit != -1 and i >= limit:
                return
            
            if instr[0] == 'x':
                self.fold_x(instr[1])
            elif instr[0] == 'y':
                self.fold_y(instr[1])
            else:
                raise Exception('how thelkjdfoiwe?')
            
            i += 1

    def get_dot_counts(self):
        return len(self.dots)
    
    def __repr__(self) -> str:
        li = []
        max_x = 0
        max_y = 0
        for dot in self.dots:
            x,y = dot
            max_x, max_y = max(max_x, x), max(max_y, y)
        for j in range(max_y+1):
            row = ['#' if (i,j) in self.dots else '.' for i in range(max_x+1)]
            li.append(''.join(row))
        return '\n'.join(li)
                

def func1(s):
    paper = Paper(s)
    # print(paper)
    # print('')

    paper.fold()
    print(paper)
    return paper.get_dot_counts()

ans1 = func1(s)

submit(DAY, 1, ans1)

# def func2(s):
#     pass
# ans2 = func2(s)

# submit(DAY, 2, ans2)
