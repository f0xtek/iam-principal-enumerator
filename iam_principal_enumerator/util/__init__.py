import random
import string


def generate_random_string(length=8):
    """
    Generate a random string of the specified length.

    :param length: Length of the random string (default is 8)
    :return: A random alphanumeric string
    """
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))