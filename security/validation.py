import re


def username_validator(text):
    username_regex = r'^(?=.*[a-zA-Z])[a-zA-Z0-9_.-]{4,30}$'
    a = re.match(username_regex, text)
    return a


def email_validator(text):
    email_regex = r'^[a-zA-Z0-9._]{2,30}@[a-zA-Z0-9.-]{2,30}\.[a-zA-Z]{2,30}$'
    a = re.match(email_regex, text)
    return a


def password_validator(text):
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z0-9!@#$%^&*()_+=\-[\]{}|\\:;"\'<>,.?/~]{8,30}$'
    a = re.match(password_regex, text)
    return a


def phone_number_validator(text):
    phone_number_regex = r'^\d{1,30}$'
    a = re.match(phone_number_regex, text)
    return a
