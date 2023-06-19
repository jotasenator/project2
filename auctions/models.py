from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64, default='')
    description = models.TextField(blank=True, default='')
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_url = models.URLField(default='')
    category = models.CharField(max_length=64, default='')
    active = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="listings")

class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids",blank=True, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", blank=True, null=True,)

class Comment(models.Model):
    text = models.TextField(default='')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments",blank=True, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments",blank=True, null=True)

