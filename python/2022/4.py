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

DAY = 4
# s = get_example(DAY).strip() # the daily input is stored in s
# print(s)
s = get_input(DAY).strip() # the daily input is stored in s


'''
Your code here
Put the result in `ans` as a str or int.
'''
def is_superset_by(superset, subset):
    return (int(superset[0]) <= int(subset[0])) and (int(superset[1]) >= int(subset[1]))

def has_intersections(first, second):
    return not ((first[0] > second[1]) or (first[1] < second[0]))
    

def func1(s):
    count = 0
    for pair in s.split('\n'):
        
        first, second = pair.split(',')
        firstRange, secondRange = first.split('-'), second.split('-')

        if is_superset_by(firstRange, secondRange) or is_superset_by(secondRange, firstRange):
            count += 1

    return count
        

ans1 = func1(s)

# submit(DAY, 1, ans1)

def func2(s):
    count = 0
    for pair in s.split('\n'):
        
        first, second = pair.split(',')
        firstRange, secondRange = list(map(int, first.split('-'))), list(map(int, second.split('-')))

        if has_intersections(firstRange, secondRange):
            count += 1

    return count
ans2 = func2(s)

submit(DAY, 2, ans2)