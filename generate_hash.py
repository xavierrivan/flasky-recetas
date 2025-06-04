from werkzeug.security import generate_password_hash

password = "12345"
password_hash = generate_password_hash(password)
print(password_hash) 