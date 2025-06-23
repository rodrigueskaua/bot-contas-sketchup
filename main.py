if __name__ == "__main__":
    from core.email_api import create_temp_email
    from core.credentials import generate_secure_password, generate_name
    from web.trimble import create_trimble_account
    
    email_data = create_temp_email()
    name = generate_name()
    password = generate_secure_password()

    email, pwd = create_trimble_account(
        email=email_data["email"],
        full_name=name,
        password=password,
        email_token=email_data["token"],
        headless=False
    )

    print("\nConta criada com sucesso!")
    print(f"📧 Email: {email}")
    print(f"🔑 Senha: {pwd}")
