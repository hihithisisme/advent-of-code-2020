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

DAY = 11
# s = get_example(DAY).strip() # the daily input is stored in s
# s = """11111
# 19991
# 19191
# 19991
# 11111"""
# print(s)
s = get_input(DAY).strip() # the daily input is stored in s

'''
Your code here
Put the result in `ans` as a str or int.
'''
class Solution:

    def __init__(self, s):
        self.flashed = set()
        self.flashing = []
        self.flashes = 0
        self.octos = []
        for line in s.split('\n'):
            octo_row = [int(c) for c in line]
            self.octos.append(octo_row)

        self.ROWS = len(self.octos)
        self.COLS = len(self.octos[0])

    def increment_energy(self, row, col):
        self.octos[row][col] += 1
        if self.octos[row][col] > 9 and (row, col) not in self.flashed:
            self.flashed.add((row, col))
            self.flashing.append((row, col))

    def flash(self, row, col):
        self.flashes += 1
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                new_row = i + row
                new_col = j + col
                if new_row < 0 or new_row >= self.ROWS or new_col < 0 or new_col >= self.COLS:
                    continue
                
                self.increment_energy(new_row, new_col)

    def step(self):
        self.flashed = set()
        self.flashing = []
        # increment all octos energy by 1
        # add all energies >9 to queue
        for row in range(self.ROWS):
            for col in range(self.COLS):
                self.increment_energy(row, col)

        # consume queue and increment all adj octos energy by 1 (adding all energies >9 to queue)
        while len(self.flashing) > 0:
            o = self.flashing.pop(0)
            self.flash(o[0], o[1])
            
        # post-flashing: time to reduce all flashed to 0
        for row, col in self.flashed:
            self.octos[row][col] = 0

        return len(self.flashed) == (self.ROWS * self.COLS)


    def get_total_flashes(self):
        return self.flashes

    def __repr__(self) -> str:
        li = []
        for i in range(self.ROWS):
            octo_row = ''.join(str(self.octos[i]))
            li.append(octo_row)
        return '\n'.join(li)



def func1(s):
    sol = Solution(s)
    for i in range(100):
        sol.step()
        # print(sol)
        # print(sol.get_total_flashes())
    
    return sol.get_total_flashes()

ans1 = func1(s)

# submit(DAY, 1, ans1)

def func2(s):
    sol = Solution(s)
    i = 1
    while True:
        if sol.step():
            return i 
        i += 1
        # print(sol)
        # print(sol.get_total_flashes())
    
    return -1

ans2 = func2(s)

submit(DAY, 2, ans2)