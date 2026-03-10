import os

def run (**args):
    print("[*] W module dirbuster.")
    files = os.listdir('.')
    return str(files)

