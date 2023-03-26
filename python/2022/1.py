from utils import get_aoc_token 

import requests

AOC_COOKIE = get_aoc_token()
YEAR = '2022'

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

DAY = 1
# s = get_example(DAY).strip() # the daily input is stored in s
# print(s)
# print('-----------')
s = get_input(DAY).strip() # the daily input is stored in s

'''
Your code here
Put the result in `ans` as a str or int.
'''
def func1(s):
    elves = []
    current_sum = 0
    for line in s.split('\n'):
        if line != '':
            current_sum += int(line)
        else:
            elves.append(current_sum)
            current_sum = 0

    elves.append(current_sum)
    return max(elves)

ans1 = func1(s)

# print('solution', ans1)
# submit(DAY, 1, ans1)

def func2(s):
    elves = []
    current_sum = 0
    for line in s.split('\n'):
        if line != '':
            current_sum += int(line)
        else:
            elves.append(current_sum)
            current_sum = 0

    elves.append(current_sum)
    elves.sort(reverse=True)
    res = 0
    for i in range(3):
        res += elves.pop(0)
    return res
ans2 = func2(s)

submit(DAY, 2, ans2)