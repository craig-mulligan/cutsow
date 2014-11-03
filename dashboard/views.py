from __future__ import division
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django import forms
from dashboard import models
from django.contrib import messages
import requests
import itertools
import operator
import collections
from django.contrib import messages
from django.db.models import Max, Min, Sum, F, Count
from forms import FSUserUpdateForm, createProduct, productUpdateForm

import os
from feed.models import Notification

# for ajax templates
from django.template.loader import render_to_string

@login_required
def personal(request):
    if request.method == 'POST':
        # checks which form they are submitting
        form = FSUserUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(request.user)
            messages.add_message(
                request, messages.INFO, "Your account has successfully been updated.")
 
    return render(request, "dashboard/personal.html", {
    })

@login_required
def create(request):
    # creates a new product
    if request.user.info.designer == False:
        return redirect('/dashboard/personal')
    else:
        if request.method == 'POST':
            form = createProduct(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(request.user)
                messages.add_message(
                    request, messages.INFO, "You have successfully created a product.")
            products = models.Product.objects.filter(user=request.user).all()
            return render(request, "dashboard/products.html", {
                "products": products,
            })
        else:
            return render(request, "dashboard/create.html", {
            })

@login_required
def edit(request, product_id):

    p = models.Product.objects.get(pk=int(product_id))

    if request.user.info.designer == False | request.user.id != p.user.id:
        return redirect('/dashboard/personal')
    else:
        if request.method == 'POST':
            if '_edit' in request.POST:
                # checks which form they are submitting
                form = productUpdateForm(request.POST, request.FILES)
                if form.is_valid():
                    product = form.save(request.user)
                    messages.add_message(
                        request, messages.INFO, "Your Product has successfully been updated.")

                p = models.Product.objects.get(pk=int(product_id))
                return render(request, "dashboard/edit.html", {
                    "product": p
                })
            elif '_delete' in request.POST:
                p.delete();
                products = models.Product.objects.filter(user=request.user).all()
                messages.add_message(
                    request, messages.INFO, "Your Product has successfully been deleted.")

                return render(request, "dashboard/products.html", {
                    "products": products,
                })
        else:

            return render(request, "dashboard/edit.html", {
                    "product": p
            })


@login_required
def products(request):
    if request.user.info.designer == False:
        return redirect('/dashboard/personal')
    else:
        products = models.Product.objects.filter(user=request.user).all().order_by('-created')
        return render(request, "dashboard/products.html", {
            "products": products,
        })

@login_required
def following(request):
    user = request.user
    follows = user.info.follows.all()
    followers = user.info.followers.all()
 
    return render(request, "dashboard/following.html", {
        "follows": follows,
        "followers": followers,
    })

@login_required
def notifications(request):
    notifications = Notification.objects.filter(recipient=request.user).all().order_by('-completed')[0:10]
    for n in notifications:
        n.notified = True
        n.save()
    return render(request, "dashboard/notifications.html", {
        "notifications": notifications,
    })

@login_required
def favourites(request):
    products = request.user.info.favourites.all().order_by('-created')[0:6]
    favourites = request.user.info.favourites.all().values_list('pk', flat=True)
    return render(request, "dashboard/favs.html", {
        "products": products,
        'favourites': favourites
    })
    
@login_required
def loadmoreN(request):
    if request.is_ajax() and request.POST:
        offset = int(request.POST.get('offset'))
        notifications = Notification.objects.filter(recipient=request.user).all().order_by('-completed')[offset:offset+10]
        for n in notifications:
            n.notified = True
            n.save()
        html = render_to_string('parts/loadmoreN.html', {'notifications': notifications })
        return HttpResponse(html)
    else:
        raise Http404

@login_required
def singleproduct(request):
    if request.method == 'POST':
        # checks which form they are submitting
        form = FSUserUpdateForm(request.POST)
        if form.is_valid():
            user = form.save(request.user)
            messages.add_message(
                request, messages.INFO, "Your account has successfully been updated.")
 
    return render(request, "dashboard/dashboard.html", {
    })