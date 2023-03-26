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

DAY = 2
# s = get_example(DAY).strip() # the daily input is stored in s
# print(s)
s = get_input(DAY).strip() # the daily input is stored in s

'''
Your code here
Put the result in `ans` as a str or int.
'''
opp_map = {
    'A': 'rock',
    'B': 'paper',
    'C': 'scissors'
}

def eval(opp, you):
    outcome = -1
    # you win scenario
    if (opp == 'A' and you == 'Y') or (opp == 'B' and you == 'Z') or (opp == 'C' and you == 'X'):
        outcome = 6
    # draw
    elif (opp == 'A' and you == 'X') or (opp == 'B' and you == 'Y') or (opp == 'C' and you == 'Z'):
        outcome = 3
    else:
        outcome = 0
    
    shape = -1
    if you == 'X':
        shape = 1
    elif you == 'Y':
        shape = 2
    else:
        shape = 3
    return shape + outcome

def func1(s):
    final_score = 0
    for pair in s.split('\n'):
        opp, you = pair.split(' ')
        score = eval(opp, you)
        final_score += score

    return final_score

ans1 = func1(s)

# print('example solution', ans1)
# submit(DAY, 1, ans1)

def eval2(opp, out):
    outcome = -1
    if out == 'X':
        outcome = 0
    elif out == 'Y':
        outcome = 3
    else:
        outcome = 6

    you = 'shape here'
    if out == 'Y':
        if opp == 'A':  # rock
            you = 'rock'
        elif opp == 'B': # paper
            you = 'paper'
        else:
            you = 'scissors'
    elif out == 'X': # lose
        if opp == 'A':  # rock
            you = 'scissors'
        elif opp == 'B': # paper
            you = 'rock'
        else:
            you = 'paper'
    else:           # win
        if opp == 'A': #rock
            you = 'paper'
        elif opp == 'B': #paper
            you = 'scissors'
        else:           # scissors
            you = 'rock'
    
    shape = -1
    if you == 'rock':
        shape = 1
    elif you == 'paper':
        shape = 2
    else:
        shape = 3
    return shape + outcome


def func2(s):
    final_score = 0
    for pair in s.split('\n'):
        opp, out = pair.split(' ')
        score = eval2(opp, out)
        final_score += score

    return final_score
ans2 = func2(s)

submit(DAY, 2, ans2)