import json

def get_aoc_token():
    try:
        with open('./env.json') as f:
            data = json.load(f)
            return data["AOC_SESSION_TOKEN"]
    except Exception as e:
        print("AOC_SESSION_TOKEN not set ", e)
