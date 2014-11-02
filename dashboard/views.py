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
    if request.user.info.designer == False:
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
        products = models.Product.objects.filter(user=request.user).all()
        return render(request, "dashboard/products.html", {
            "products": products,
        })

@login_required
def following(request):
    if request.method == 'POST':
        # checks which form they are submitting
        form = FSUserUpdateForm(request.POST)
        if form.is_valid():
            user = form.save(request.user)
            messages.add_message(
                request, messages.INFO, "Your account has successfully been updated.")

    follows = request.user.info.follows
 
    return render(request, "dashboard/following.html", {
        "follows": follows,
    })

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