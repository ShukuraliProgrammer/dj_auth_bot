import secrets

def generate_code():
    number = '123456789'
    return ''.join(secrets.choice(number) for i in range(6))