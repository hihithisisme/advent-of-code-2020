import re
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

DAY = 17
# s = get_example(DAY).strip() # the daily input is stored in s
# print(s)
s = get_input(DAY).strip() # the daily input is stored in s

'''
Your code here
Put the result in `ans` as a str or int.
'''
'''
Observations:
- x, y are the initial velocity
- x and y vectors are independent of each other; hence we can break this into 2 sub-problems
    - initial x needs to be set such that it is possible for some step to land within the target area
    - initial y can be used to maximize the height

what we need:
- def get_max_height(x,y) -> int
- def is_too_fast(x) -> boolean

Approaches:
- Brute force: To iterate all x values to find all feasible x values
    - For each of these, iterate through y values in order to find the max max_height
    - contingent on not many x values

- Mathematical approach:
    - xt(t) = xi + xi + (xi-1) + (xi-2) + ... + (xi-(t-1))
            = (t+1) * xi - (t * (t-1) / 2)
    - yt(t) = y0 + y0-1 + y0-2 + ... + y0-(t-1)
            = (t+1) * y0 - t

'''

def xt(t, x0):
    add = 0
    for i in range(1, t+1):
        add += max(x0 - (i - 1), 0)
    return add

def yt(t, y0):
    return t * y0 - (t * (t-1) / 2)

def pos_t(t, x0, y0):
    return (xt(t, x0), yt(t, y0))

def get_max_height(y0):
    # we get max_height when y vel == 0
    if y0 < 0:
        return y0
    t = y0
    # print((y0**2 + y0)/2)
    return yt(t, y0)


def func1(s):
    match = re.search('target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)', s)
    xmin, xmax, ymin, ymax = list(map(int, match.group(1, 2, 3, 4)))

    # returns a list of t values where the probe will be within the target area for the x-axis
    def when_land_x():
        res = {}
        for x0 in range(1, xmax+1):
            t, x = 1, x0
            possible_t = []
            prev_x = -1

            while x <= xmax and prev_x != x:
                # print(x0, x)
                if x >= xmin:
                    possible_t.append(t)

                t += 1
                prev_x = x
                x = xt(t, x0)

            if len(possible_t) > 0:
                if prev_x == x and xmin <= xt(possible_t[-1], x0) <= xmax:
                    possible_t.append(-1)
                res[x0] = possible_t

        return res
    
    def will_land_y(ts, y0):
        prev_t = None
        for t in ts:
            if t == -1:
                t = prev_t + 1
                y = yt(t, y0)

                while y >= ymin:
                    if y <= ymax:
                        return True
                    t += 1
                    y = yt(t, y0)

                return False
            else:
                y = yt(t, y0)
                if y >= ymin and y <= ymax:
                    return True
                prev_t = t
                
        return False
    
    m = when_land_x()

    possible_ys = []
    possible_vels = set()
    for x0, ts in m.items():
        # print('processing', x0, ts)
        # max y that we have to check for is abs(ymax)
        for y0 in range(ymin, abs(ymin)+1):
            if will_land_y(ts, y0):
                # print(y0, get_max_height(y0))
                possible_ys.append((y0, get_max_height(y0)))
                possible_vels.add((x0,y0))
    # print(possible_vels)
    # print(list(filter(lambda pos: pos[1] == -10, possible_vels)))
    # return int(max([item[1] for item in possible_ys]))
    return len(possible_vels)
    


# print(len('....................#') + 6)
print(s)
# print(get_max_height(2))

# ans1 = func1(s)
# submit(DAY, 1, ans1)

# def func2(s):
#     pass
s = 'target area: x=282184..482382, y=-502273..-374688'
ans2 = func1(s)
submit(DAY, 2, ans2)