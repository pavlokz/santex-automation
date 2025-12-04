import random
import string

def random_name(length: int = 6) -> str:
    return ''.join(random.choices(string.ascii_letters, k=length))

def zip_code_numeric() -> str:
    return ''.join(random.choices(string.digits, k=5))

# Example sets for checkout parametrization
checkout_examples = [
    ("Pablo", "Quesada", "10001"),
    ("Ana", "Perez", "20002"),
    (random_name(), random_name(), zip_code_numeric()),
]