import requests
from faker import Faker
import random
import string

def create_temp_email():
    domain = requests.get("https://api.mail.tm/domains").json()["hydra:member"][0]["domain"]
    fake = Faker()
    username = fake.user_name() + ''.join(random.choices(string.digits, k=3))
    email = f"{username}@{domain}"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))

    resp = requests.post("https://api.mail.tm/accounts", json={"address": email, "password": password})
    if resp.status_code != 201:
        raise Exception("Erro ao criar email temporário")

    token_resp = requests.post("https://api.mail.tm/token", json={"address": email, "password": password})
    token = token_resp.json()["token"]
    return {"email": email, "password": password, "token": token}
