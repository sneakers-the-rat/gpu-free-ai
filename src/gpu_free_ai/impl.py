import random
import string


def __getattr__(name):
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


class AI:
    def __init__(self, *args, **kwargs):
        # input is irrelevant
        pass

    def __call__(self, *args, **kwargs):
        return _anything()

    def __getattr__(self, name):
        """
        sometimes things are attributes, sometimes things are methods.
        """
        if random.random() > 0.5:
            return _anything()
        else:
            return AI()
