from django.shortcuts import render, redirect
from .models import User, Appointment
from datetime import datetime
from django.utils import timezone
from django.contrib import messages
import pytz

def index(request):
	#renders the login and register page

	#uncomment to nuke the databases
	# User.userManager.all().delete()
	# Appointment.appointmentManager.all().delete()

	return render(request, 'appointment_app/index.html')

def register(request):
	user = User.userManager.register(request.POST['uname'], request.POST['email'], request.POST['pw'], request.POST['cpw'], request.POST['dob'])
	if user[0]:
		request.session['user'] = (user[2], user[3])
		return redirect('/appointments')
	else:
		for message in user[1]:
			messages.add_message(request, messages.ERROR, message)
		return redirect('/')

def login(request):
	user = User.userManager.login(request.POST['email'], request.POST['pw'])
	if user[0]:
		if user[1]:
			request.session['user'] = (user[2], user[3])
			return redirect('/appointments')
	else:
		for message in user[1]:
			messages.add_message(request, messages.ERROR, message)
		return redirect('/')

def logoff(request):
	request.session.clear()
	return redirect('/')

def appointments(request):
	appointments = Appointment.appointmentManager.filter(user = request.session['user'][0]).order_by('when')
	today = []
	later = []
	now = datetime.now()
	now = now.replace(tzinfo=pytz.UTC)
	for appointment in appointments:
		if now.date() == appointment.when.date():
			today.append(appointment)
		elif appointment.when.date() > now.date():
			later.append(appointment)
		# else:
		# 	Appointment.appointmentManager.filter(id=appointment.id).delete()
		# 	print 'deleting an old appointment'
	return render(request, 'appointment_app/home.html', {'now': now, 'today': today, 'later': later})

def create(request):
	appointment = Appointment.appointmentManager.newAppointment(request.session['user'][0], request.POST['date'], request.POST['time'], request.POST['task'])
	if not appointment[0]:
		for message in appointment[1]:
			messages.add_message(request, messages.ERROR, message)
	return redirect('/appointments')

def edit(request, id):
	appointment = Appointment.appointmentManager.get(id=id)
	appointment.date = datetime.strftime(appointment.when, '%Y-%m-%d')
	appointment.time = datetime.strftime(appointment.when, '%H:%M')
	return render(request, 'appointment_app/edit.html', {'appointment': appointment})

def update(request, id):
	appointment = Appointment.appointmentManager.updateAppointment(request.session['user'][0], id, request.POST['date'], request.POST['time'], request.POST['task'], request.POST['status'])
	if not appointment[0]:
		for message in appointment[1]:
			messages.add_message(request, messages.ERROR, message)
		return redirect('/appointments/{}'.format(id))
	return redirect('/appointments')

def delete(request, id):
	Appointment.appointmentManager.filter(id=id).delete();
	return redirect('/appointments')