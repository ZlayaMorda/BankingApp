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
            code = Code.generate_code_6()
            cache.set(code, jwt)
            return code
        except:
            raise Exception("Code can't be set")

    @staticmethod
    def load(code: str):
        return cache.get(code)
