from random import randint

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

FORM_EMAIL = 'your_email@gmail.com'
EMAIL_ADMIN = 'your_email@gmail.com'


def create():
    password_new = ''
    for i in range(8):
        password_new += chr(randint(63, 122))
    return password_new


create()
