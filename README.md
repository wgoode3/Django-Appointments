# Django-Appointments
Appointment keeping app using Django with some Bootstrap

## How to get it running
1. Make sure Python and pip are installed. On a Debian/Ubuntu based OS:
```
$ sudo apt-get update
$ sudo apt-get install python-pip
```
2. Create a virtual environment for Django and install requirements:
```
$ sudo apt-get update
$ pip install virtualenv
$ cd ~/Django-Appointments
$ virtualenv djangoenv
$ source djangoenv/bin/activate
$ pip install -r requirements.txt
```
3. Run the server:
```
$ python manage.py runserver
```
