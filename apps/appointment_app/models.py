from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime
import pytz

PASSWORD_REGEX = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def register(self, uname, email, pw, cpw, dob):
		message = []
		if len(uname) < 1:
			message.append('Username cannot be blank!')
		if len(email) < 1:
			message.append('Email cannot be blank!')
		else:
			if not EMAIL_REGEX.match(email):
				message.append('Invalid email address!')
		check = User.userManager.filter(uname=uname)
		if len(check) > 0:
			message.append('Username already exists!')
		check = User.userManager.filter(email=email)
		if len(check) > 0:
			message.append('Email already exists!')
		if len(pw) < 1:
			message.append('Password cannot be blank!')
		else:
			if not PASSWORD_REGEX.match(pw):
				message.append('Password must be 8 characters or more with at least one capital letter, lowercase letter, and number!')
		if pw != cpw:
			message.append('Password does not match confirm password!')
		if len(dob) < 1:
			message.append('Date of Birth is required!')
		else:
			now = datetime.now()
			dob = datetime.strptime(dob, '%Y-%m-%d')
			if dob > now:
				message.append('Date of Birth must be in the past!')

		if len(message) > 0:
			return (False, message)
		else:
			pw_hash = bcrypt.hashpw(str(pw), bcrypt.gensalt())
			user = User.userManager.create(uname=uname, email=email, pw_hash=pw_hash, dob=dob) 
			return (True, user, user.id, user.uname)
	
	def login(self, email, pw):
		message = []
		if len(email) < 1:
			message.append('Email cannot be blank!')
		else:
			if not EMAIL_REGEX.match(email):
				message.append('Invalid email address!')
		if len(pw) < 1:
			message.append('Password cannot be blank!')
		else:
			if not PASSWORD_REGEX.match(pw):
				message.append('Password must be 8 characters or more with at least one capital letter, lowercase letter, and number!')
		
		if len(message) < 1:
			login = User.userManager.filter(email=email)
			if len(login) < 1:
				message.append('email not in database')
			else:
				if bcrypt.checkpw(str(pw), str(login[0].pw_hash)):
					return (True, login, login[0].id, login[0].uname)
				else:
					message.append('wrong password dude')

		return (False, message)

class AppointmentManager(models.Manager):
	def newAppointment(self, user, date, time, task):
		message = []
		if len(date) < 1:
			message.append('Date is required!')
		if len(time) < 1:
			message.append('Time is required!')
		if len(date) > 1 and len(time) > 1:
			when = date + " " + time
			when = datetime.strptime(when, '%Y-%m-%d %H:%M')
			now = datetime.now()
			if when < now:
				message.append('Appointment must be in the future!')
			appointments = Appointment.appointmentManager.filter(user = user)
			when = when.replace(tzinfo=pytz.UTC)
			for appointment in appointments:
				if appointment.when == when:
					message.append('You already have an appointment at that time!')
		if len(task) < 8:
			message.append('Task must be 8 characters or more.')

		if len(message) < 1:
			appointment = Appointment.appointmentManager.create(user_id=user, when=when, task=task, status='pending')
			return(True, appointment)
		
		return (False, message)
	def updateAppointment(self, user, id, date, time, task, status):
		message = []
		if len(date) < 1:
			message.append('Date is required!')
		if len(time) < 1:
			message.append('Time is required!')
		if len(date) > 1 and len(time) > 1:
			when = date + " " + time
			when = datetime.strptime(when, '%Y-%m-%d %H:%M')
			now = datetime.now()
			if when < now:
				message.append('Appointment must be in the future!')
			appointments = Appointment.appointmentManager.filter(user = user)
			appointments = appointments.exclude(id=id)
			when = when.replace(tzinfo=pytz.UTC)
			for appointment in appointments:
				if appointment.when == when:
					message.append('You already have an appointment at that time!')
		if len(task) < 8:
			message.append('Task must be 8 characters or more.')

		if len(message) < 1:
			appointment = Appointment.appointmentManager.filter(id=id).update(when=when, task=task, status=status)
			return(True, appointment)
		
		return (False, message)

class User(models.Model):
	uname = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	pw_hash = models.CharField(max_length=255)
	dob = models.DateTimeField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	userManager = UserManager()

class Appointment(models.Model):
	user = models.ForeignKey(User)
	when = models.DateTimeField()
	task = models.CharField(max_length=255)
	status = models.CharField(max_length=255)
	appointmentManager = AppointmentManager()
