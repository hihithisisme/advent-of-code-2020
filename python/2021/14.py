import collections
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

DAY = 14
# s = get_example(DAY).strip() # the daily input is stored in s
# print(s)
s = get_input(DAY).strip() # the daily input is stored in s

'''
Your code here
Put the result in `ans` as a str or int.
'''

""" 
Unoptimized approach (brute force)
- exponential complexity (time and space) due to the exponential growth

Taking steps as N, and initial template size as M:
- Complexity is O( (M-1) * 2^N +1 ) = O(M * 2^N)
"""
def func(s, steps):
    lines = s.split('\n')
    template = list(lines[0])
    inserts = {}
    for line in lines[2:]:
        match = re.search('([A-Z]+) -> ([A-Z])', line)
        if match == None:
            raise Exception('unexpected')
        
        inserts[match.group(1)] = match.group(2)

    for step in range(steps):
        new_template = []
        for idx in range(len(template)-1):
            insert = inserts[''.join(template[idx:idx + 2])]
            new_template.append(template[idx])
            new_template.append(insert)

        new_template.append(template[len(template)-1])

        template = new_template

    counter = collections.Counter(new_template)
    most, least = 0, 9**9
    for v in counter.values():
        most = max(most, v)
        least = min(least, v)

    return most - least

"""
Uses hashmap to store the template since we only really care about the number of letter pairs
Compute the frequency of letters at the end by dividing all by 2
- consider first and last letter will appear 1 less (can +1)
- first and last letter will always remain in their position due to nature of adding letters

Taking steps as N, and initial template size as M:
- Assuming in the worst case scenario where the initial template is made up of all unique letters:
- Max hashmap size is 2 * M * (M-1) + M = 2M^2 - M = O(M^2) -- space complexity
- Time complexity: O(N * M^2)
"""
def func2(s, steps):
    lines = s.split('\n')
    template_line = list(lines[0])
    template = collections.Counter()

    for idx in range(len(template_line)-1):
        template[''.join(template_line[idx:idx+2])] += 1

    inserts = {}
    for line in lines[2:]:
        # match = re.search('([A-Z]+) -&gt; ([A-Z])', line)
        match = re.search('([A-Z]+) -> ([A-Z])', line)
        if match == None:
            raise Exception('unexpected')
        
        inserts[match.group(1)] = match.group(2)

    for step in range(steps):
        new_template = collections.Counter()
        
        for key in template:
            insert = inserts[key]
            new_template[key[0]+insert] += template[key]
            new_template[insert+key[1]] += template[key]

        template = new_template

    counter = collections.Counter()
    for key in template:
        counter[key[0]] += template[key]
        counter[key[1]] += template[key]
    counter[template_line[0]] += 1
    counter[template_line[-1]] += 1
    for key in counter:
        if counter[key] % 2 != 0:
            raise Exception('how come this is not even number?', key, counter)
        counter[key] = int(counter[key]/2)

    most, least = counter[template_line[0]], counter[template_line[0]]
    for v in counter.values():
        most = max(most, v)
        least = min(least, v)

    return most - least

# ans1 = func2(s, 10)

# submit(DAY, 1, ans1)

# def func2(s):
#     pass
ans2 = func2(s, 40)

submit(DAY, 2, ans2)