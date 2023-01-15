# Оnline store from the Slime Rancher

The store has registration, authorization, product catalog, shopping cart.

Thesis for a course in the profession of Python-developer.
Fan site selling plorts from the Slime Rancher game.
Only we have the freshest plorts from 'Far, Far Range'!

## For the project to work correctly:

After cloning the project to your device, make sure that the database you need is set in 
the [settings.py](https://github.com/DaryaKhatsuk/Online-store/blob/master/graduarion_project/graduarion_project/settings.py) 
file, in *DATABASES*, the database you need is installed.

Further, in the lines:

  EMAIL_HOST_USER = 'your_email@gmail.com'
  
  EMAIL_HOST_PASSWORD = 'your_password'
  
  FORM_EMAIL = 'your_email@gmail.com'
  
  EMAIL_ADMIN = 'your_email@gmail.com'
  
Enter the email and password you need

Also specify them in the file: [helper_file.py](https://github.com/DaryaKhatsuk/Online-store/blob/master/graduarion_project/site1/helper_file.py)

In the [parser_for_bases.py](https://github.com/DaryaKhatsuk/Online-store/blob/master/graduarion_project/site1/management/commands/parser_for_bases.py) 
file, change the *path to the plorts.txt* file to match the path on your device and run the file through *the terminal* of the python interpreter.
