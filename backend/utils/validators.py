import re

password_regex = re.compile(r"^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{8,}$")
email_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def validate_password(password: str) -> str:
    if not password_regex.match(password):
        raise ValueError(
            "Password must have at least 8 characters, uppercase, lowercase, number and special character"
        )
    return password


def validate_email(email: str) -> str:
    if not email_regex.match(email):
        raise ValueError("Invalid email address")
    return email
