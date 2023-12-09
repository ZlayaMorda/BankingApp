import random
from django.core.cache import cache


class Code:

    @staticmethod
    def generate_code_6() -> str:
        code = (((((str(random.randint(0, 9)) +
                str(random.randint(0, 9))) +
                str(random.randint(0, 9))) +
                str(random.randint(0, 9))) +
                str(random.randint(0, 9))) +
                str(random.randint(0, 9)))

        # TEMP
        print(code)
        return code

    @staticmethod
    def store(jwt: str):
        try:
            cache.set(Code.generate_code_6(), jwt)
        except:
            raise Exception("Code can't be set")

    @staticmethod
    def load(code: str):
        return cache.get(code)
