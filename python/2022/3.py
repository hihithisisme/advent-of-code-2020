from utils import get_aoc_token
from collections import Counter

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

DAY = 3
# s = get_example(DAY).strip() # the daily input is stored in s
# print(s)
s = get_input(DAY).strip() # the daily input is stored in s

'''
Your code here
Put the result in `ans` as a str or int.
'''
def get_priority(letter):
    if letter.islower():
        return ord(letter) - 96
    else:
        return ord(letter) - 64 + 26

def get_common_letter(first, second):
    counter = Counter(first)

    for letter in second:
        if letter in counter:
            return letter

    return None

def get_common_letter_from_group(group):
    counter0 = Counter(group[0])
    counter1 = Counter(group[1])

    for letter in group[2]:
        if letter in counter0 and letter in counter1:
            return letter

    return None
    
def func1(s):
    ans = 0
    for sack in s.split('\n'):
        if sack == '': continue
        first = sack[:int(len(sack)/2)]
        second = sack[int(len(sack)/2):]
        common_letter = get_common_letter(first, second)
        
        ans += get_priority(common_letter)

    return ans
        
ans1 = func1(s)

# print('example solution', ans1)
# submit(DAY, 1, ans1)

def func2(s):
    ans = 0
    elves = s.split('\n')
    for idx in range(2, len(elves), 3):
        group = elves[idx-2 : idx+1]
        common_letter = get_common_letter_from_group(group)
        ans += get_priority(common_letter)

    return ans

ans2 = func2(s)

submit(DAY, 2, ans2)