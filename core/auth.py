import requests
import time
import re

def extract_code_from_email(text):
    print("Extraindo código do texto do email...")
    print(f"Texto recebido para extrair código:\n{text}\n")
    pattern = r"código de verificação.*?é:\s*([\d]{6})"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        print(f"Código encontrado: {match.group(1)}")
        return match.group(1)
    else:
        print("Nenhum código encontrado no texto.")
        return None

def wait_for_verification_code(token, timeout_seconds=60):
    headers = {"Authorization": f"Bearer {token}"}
    for _ in range(timeout_seconds // 2):
        resp = requests.get("https://api.mail.tm/messages", headers=headers)
        messages = resp.json().get("hydra:member", [])
        if messages:
            msg_id = messages[0]["id"]
            msg = requests.get(f"https://api.mail.tm/messages/{msg_id}", headers=headers).json()
            code = extract_code_from_email(msg.get("text", ""))
            if code:
                return code
        time.sleep(2)
    raise TimeoutError("Código de verificação não chegou a tempo")
