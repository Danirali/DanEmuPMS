import bcrypt
plain_text = input("Enter password in plain text: \n")

hashed_password = bcrypt.hashpw(plain_text.encode('utf-8'), bcrypt.gensalt())
print(f"Hashed Password: {hashed_password.decode()}")