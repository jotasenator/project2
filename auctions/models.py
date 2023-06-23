from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    pass


def get_default_deadline():
    return timezone.now() + timedelta(hours=3)


class Listing(models.Model):
    title = models.CharField(max_length=64, default="")
    description = models.TextField(blank=True, default="")
    starting_bid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Starting bid: ($US)"
    )
    image_url = models.URLField(default="")
    category = models.CharField(max_length=64, default="")
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="listings",
    )
    deadline = models.DateTimeField(default=get_default_deadline)


class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids", blank=True, null=True
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="bids",
        blank=True,
        null=True,
    )


class Comment(models.Model):
    text = models.TextField(default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,default=None)
    created_at = models.DateTimeField(default=timezone.now)


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    listings = models.ManyToManyField(Listing)
