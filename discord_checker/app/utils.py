import itertools
import json

def load_tokens(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def load_proxies(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return itertools.cycle([line.strip() for line in f if line.strip()])

def save_to_file(filename, token, user_data):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps({"token": token, **user_data}, ensure_ascii=False) + "\n")