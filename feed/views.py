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
from dashboard.models import Product
from feed import models
from django.db.models import Max, Min, Sum, F, Count

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

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


def singleproduct(request, product_id):
    p = Product.objects.get(pk=int(product_id))
    return render(request, "feed/singleproduct.html", {
        "p": p
    })

def profile(request, user_id):
    user = User.objects.get(pk=int(user_id))
    products = Product.objects.filter(user=user).all()
    followers = user.info.followers.count()

    return render(request, "feed/userprofile.html", {
        "user": user,
        "products": products,
        "viewer": request.user,
        "followers" : followers
    })

@login_required
def follow(request):
    if request.is_ajax() and request.POST:
        follower = User.objects.get(pk=int(request.POST.get('follower')))
        designer = User.objects.get(pk=int(request.POST.get('designer')))
        designer.info.followers.add(follower)
        designer.info.save()
        designer.save()

        data = {'message': "%s added" % designer}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404

def followerlisting(request, user_id):
    print user_id
    user = User.objects.get(pk=int(user_id))
    followers = user.info.followers.all()
    return render(request, "feed/followerslisting.html", {
        "user": user,
        "followers" : followers
    })


@login_required
def userfeed(request):
    products = Product.objects.all()
    return render(request, "feed/index.html", {
      "products": products,
    })