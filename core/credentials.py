import random
import string
from faker import Faker

def generate_secure_password(length=12):
    lowercase = random.choice(string.ascii_lowercase)
    uppercase = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*()-_=+[]{}|;:,.<>?")

    remaining = ''.join(random.choices(
        string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?",
        k=length - 4
    ))

    password = list(lowercase + uppercase + digit + special + remaining)
    random.shuffle(password)
    return ''.join(password)

def generate_name():
    return Faker().name()
