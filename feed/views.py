from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail

from django.shortcuts import render
from django.views import generic
from forms import FSUserForm
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
import os

from feed import functions


def register(request):
    if request.method == 'POST':
        form = FSUserForm(request.POST)
        key = functions.unique_key()
        if form.is_valid():
            new_user = form.save()
            if new_user is False:
                messages.add_message(request, messages.INFO, "Email already exists")
                return render(request, "registration/register.html")
            try:
                email = request.POST["email"]
            except:
                print "No email in post WTF"
                raise

            message_body = """
            <p>Hi %s,</p>
            <p>Please click on the link below to confirm your account:</p>
            <p>http://%s/confirm/%s</p><br>
            <p>Any questions? Please email us at info@4diprivaca.com</p>""" % (new_user.first_name, request.get_host(), key)
            string = (
                new_user.first_name + " " + new_user.last_name,
                new_user.email,
            )
            privaca_body = """
            <p><strong>User details:</strong></p>
            <ul>
                <li><strong>Name:</strong> %s</li>
                <li><strong>Email:</strong> %s</li>
            </ul>""" % string

            # Send email to user
            send_mail('Subject here', message_body, 'craig.andrew.mulligan@gmail.com',[email], fail_silently=False)

            # Send email to admin
            # tasks.send_email.delay("New signup", privaca_body, "craig@firingsquad.co.za")

            print "tits"
            # One week til it expires
            cache.set(key, email, 604800)

            return render(request, "registration/registered.html")
        else:
            messages.add_message(
                request, messages.INFO, "Form is incomplete.")
    form = FSUserForm()
    return render(request, "registration/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


def confirm(request, key=None):
    print key
    if key:
        email = cache.get(key)
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        messages.add_message(
            request, messages.INFO, "Account confirmed. Please log in at /login")

    return redirect(reverse("index"))


def index(request):
    return redirect("/feed")

@login_required
def userfeed(request):
    return render(request, "feed/index.html", {
      
    })