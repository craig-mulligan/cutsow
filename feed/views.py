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
from models import Notification

# for ajax templates
from django.template.loader import render_to_string


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
    if request.method == 'POST':
        print request.user.email
        subject = request.POST['subject']
        message_body = "Location: "+request.POST['location']
        message_body += "Message: "+request.POST['subject']
        from_email = request.user.email
        to_email = 'craig.andrew.mulligan@gmail.com'
        send_mail(subject, message_body, from_email, [to_email], fail_silently=False)
        messages.add_message(
            request, messages.INFO, "Email successfully sent!")

    p = Product.objects.get(pk=int(product_id))
    dopers = p.dopers.all()
    # list of favourites to check against for dope button
    favourites = request.user.info.favourites.all().values_list('pk', flat=True)
    return render(request, "feed/singleproduct.html", {
        "p": p,
        "dopers": dopers,
        "favourites": favourites,
    })

    

def profile(request, user_id):
    designer = User.objects.get(pk=int(user_id))
    products = Product.objects.filter(user=designer).all()
    followers = designer.info.followers.count()
    # creates a list of followers for template conditionals
    followcheck = designer.info.followers.all().values_list('pk', flat=True)
    favourites = request.user.info.favourites.all().values_list('pk', flat=True)
    return render(request, "feed/userprofile.html", {
        "userprofile": designer,
        "products": products,
        "user": request.user,
        "followers" : followers,
        'followcheck': followcheck,
        "favourites": favourites,

    })

@login_required
def follow(request):
    if request.is_ajax() and request.POST:
        follower = User.objects.get(pk=int(request.POST.get('follower')))
        designer = User.objects.get(pk=int(request.POST.get('designer')))
        #check if follow or unfollow button fired
        if  designer.info.followers.filter(pk=follower.id).exists():
            designer.info.followers.remove(follower)
            designer.info.save()
            designer.save()
            # add the designer to users following list
            follower.info.follows.remove(designer)
            follower.info.save()
            follower.save()
            followcount = designer.info.followers.count()
            functions.notify(request, designer, follower, None, "unfollowed you")

            data = {
                'message': 'unfollowed',
                'followcount' : followcount 
            }

        else:
            # add the user to designers followers list
            designer.info.followers.add(follower)
            designer.info.save()
            designer.save()
            # add the designer to users following list
            follower.info.follows.add(designer)
            follower.info.save()
            follower.save()
            followcount = designer.info.followers.count()
            data = {
                'message': 'followed',
                'followcount' : followcount 
            }

            functions.notify(request, designer, follower, None, "followed you")

        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404

@login_required
def dope(request):
    if request.is_ajax() and request.POST:
        user = request.user
        product = Product.objects.get(pk=int(request.POST.get('product')))
        designer = product.user
        #check if they have already voted
        if product.dopers.filter(pk=user.id).exists():
        #check if follow or unfollow button fired
            product.dopers.remove(user)
            user.info.favourites.remove(product)
            # recalculate the rating
            product.rating = product.dopers.count()
            # create notification
            n = Notification.objects.get(recipient=designer.id, actor=user, product=product)
            n.delete()
            data = {
                'message': 'undope',
                'rating': product.rating,
            }
        else: 
            product.dopers.add(user)
            user.info.favourites.add(product)
            product.rating = product.dopers.count()
            # create notification
            functions.notify(request, designer, user, product, "doped")
            data = {
                'message': 'dope',
                'rating': product.rating
            }


        product.save()
        user.info.save()
        user.save()
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404

def followerlisting(request, user_id):
    user = User.objects.get(pk=int(user_id))
    followers = user.info.followers.all()

    return render(request, "feed/followerslisting.html", {
        "followed": user,
        "followers" : followers,

    })

    
@login_required
def loadmore(request):
    if request.is_ajax() and request.POST:
        offset = int(request.POST.get('offset'))
        feedtype = request.POST.get('type')
        favourites = request.user.info.favourites.all().values_list('pk', flat=True)
        # pull products depending on feed type
        if feedtype == "popular":
            products = Product.objects.all().order_by('-rating')[offset:offset+3]
        elif feedtype == "userfeed":
            designers = request.user.info.follows.all()
            products = Product.objects.filter(user=designers).all().order_by('-created')[offset:offset+3]
        elif feedtype == "latest":
            products = Product.objects.all().order_by('-created')[offset:offset+3]
        elif feedtype == "favourites":
            products = request.user.info.favourites.all().order_by('-created')[offset:offset+3]

        html = render_to_string('parts/productloop.html', {'products': products, "favourites": favourites})
        return HttpResponse(html)
    else:
        raise Http404

@login_required
def userfeed(request):
    designers = request.user.info.follows.all()
    products = Product.objects.filter(user=designers).all().order_by('-created')[0:3]
    # list of favourites to check against for dope button
    favourites = request.user.info.favourites.all().values_list('pk', flat=True)
    return render(request, "feed/index.html", {
      "products": products,
      "favourites": favourites,
    })

def latest(request):
    products = Product.objects.all().order_by('-created')[0:3]
     # list of favourites to check against for dope button
    favourites = request.user.info.favourites.all().values_list('pk', flat=True)
    return render(request, "feed/index.html", {
      "products": products,
      "favourites": favourites,
    })

def popular(request):
    products = Product.objects.all().order_by('-rating')[0:3]
    # creates a list of followers for template conditionals
    favourites = request.user.info.favourites.all().values_list('pk', flat=True)
    return render(request, "feed/index.html", {
      "products": products,
      "favourites": favourites,
    })