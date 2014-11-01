from django.utils.translation import ugettext, ugettext_lazy as _
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
import feed.models
from dashboard import models
import datetime

class FSUserUpdateForm(forms.ModelForm):
    """
    A form that updates a user, from the given userID and
    password.
    """

    class Meta:
        model = User
        fields = ("email",)

    email = forms.EmailField()
    phone = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    twitter = forms.CharField(required=False)
    password = forms.CharField(required=False)
    avatar = forms.ImageField(required=False)

    def save(self, user):
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if user.info:
            user.info.phone = self.cleaned_data["phone"]
            user.info.twitter = self.cleaned_data["twitter"]
            user.info.avatar = self.cleaned_data["avatar"]
        else:
            i = models.Info(phone=self.cleaned_data["phone"], twitter=self.cleaned_data[
                            "twitter"],avatar=self.cleaned_data[
                        "avatar"], user=user)
            i.save()
        print self.cleaned_data["avatar"]
            
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])
        user.info.save()
        user.save()
        return user

class createProduct(forms.ModelForm):
    """
    A form that updates a user, from the given userID and
    password.
    """

    class Meta:
        model = User
        fields = ("email",)

    title = forms.CharField()
    description = forms.CharField()
    image = forms.ImageField()


    def save(self, user):
        print "tits"
        product = models.Product(title=self.cleaned_data["title"], description=self.cleaned_data[
                        "description"], image=self.cleaned_data[
                        "image"], user=user)
        product.save()
        return product


class productUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)

    title = forms.CharField()
    description = forms.CharField()
    productid = forms.CharField()
    image = forms.ImageField(required=False)

    def save(self, user):
        product = models.Product.objects.get(pk=int(self.cleaned_data["productid"]))
        product.title = self.cleaned_data["title"]
        product.description = self.cleaned_data["description"]
        if self.cleaned_data["image"]:
            product.image = self.cleaned_data["image"]
        product.save()
        return product