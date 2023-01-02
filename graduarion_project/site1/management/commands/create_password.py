from random import randint
from graduarion_project.graduarion_project.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, FORM_EMAIL
print(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, FORM_EMAIL
      )

def create(id_user):
    print(id_user)
    password_new = (chr(randint(97, 122)) +
                    chr(randint(33, 123)) +
                    chr(randint(63, 117)) +
                    chr(randint(33, 123)) +
                    chr(randint(33, 123)) +
                    chr(randint(63, 123)) +
                    chr(randint(33, 123)) +
                    chr(randint(97, 122))
                    )
    print(password_new)

