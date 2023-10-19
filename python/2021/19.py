import collections
from utils import get_aoc_token

import requests

AOC_COOKIE = get_aoc_token()
YEAR = '2021'


def get_input(day):
    req = requests.get(f'https://adventofcode.com/{YEAR}/day/{day}/input',
                       headers={'cookie': 'session='+AOC_COOKIE})
    return req.text


def get_example(day, offset=0):
    req = requests.get(f'https://adventofcode.com/{YEAR}/day/{day}',
                       headers={'cookie': 'session='+AOC_COOKIE})
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
                             headers={'cookie': 'session='+AOC_COOKIE}, data=data)
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


DAY = 19
s = get_example(DAY).strip()  # the daily input is stored in s
# s = get_input(DAY).strip() # the daily input is stored in s

'''
Your code here
Put the result in `ans` as a str or int.
'''


def parse_input(s):
    scanners = []
    for line in s.split('\n'):
        if line == '':
            continue
        if line[:3] == '---':
            scanners.append([])
        else:
            pos = tuple(map(int, line.split(',')))
            scanners[-1].append(pos)

    return scanners


def coord_diff(pos0, pos1):
    res = []
    res.append((pos0[0] - pos1[0], pos0[1] - pos1[1]))
    res.append((pos0[0] - pos1[1], pos0[1] - pos1[0]))
    res += [tuple(map(lambda x: -1*x, r)) for r in res]

    return res


def func1(s):
    input = parse_input(s)
    m = collections.Counter()

    for pos0 in input[0]:
        for pos1 in input[1]:
            for coord in coord_diff(pos0, pos1):
                m[coord] += 1

    for key, value in m.items():
        if value >= 3:
            print(key, value)


# ans1 = func1(s)

# submit(DAY, 1, ans1)

# def func2(s):
#     pass
# ans2 = func2(s)

# submit(DAY, 2, ans2)
