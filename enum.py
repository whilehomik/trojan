import os


def run (**args):
    print("[*] W module dirbuster.")
    res = os.system("id; ifconfig; tree")
    return str(res)