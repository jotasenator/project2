from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Bid, Comment
from django.contrib.auth.decorators import login_required

from .forms import ListingForm

from django.utils import timezone


def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            return redirect("index")
    else:
        form = ListingForm()
    return render(request, "auctions/create.html", {"form": form})


@login_required
def wishlist(request):
    return render(request, "auctions/wishlist.html")


# winner calculation for using on listing and bids functions
def get_winner(listing):
    winner = None
    winner_bid_amount = None
    if timezone.now() > listing.deadline:
        all_bids = Bid.objects.filter(listing=listing)
        if all_bids:
            winning_bid = all_bids.order_by("-bid_amount").first()
            winner = winning_bid.bidder
            winner_bid_amount = winning_bid.bid_amount
    return winner, winner_bid_amount


def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    deadline_str = listing.deadline.isoformat()
    time_remaining = listing.deadline - timezone.now()
    time_remaining_str = str(time_remaining).split(".")[0]
    if time_remaining.total_seconds() <= 0:
        time_remaining_str = "Bidding has ended"
    winner, winner_bid_amount = get_winner(listing)

    if request.method == "POST":
        bid_amount = request.POST["bid_amount"]
        bidder = request.user
        bid = Bid(bid_amount=bid_amount, bidder=bidder, listing=listing)
        bid.save()
        return redirect("listing", listing_id=listing_id)

    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "deadline_str": deadline_str,
            "time_remaining": time_remaining_str,
            "winner": winner,
            "winner_bid_amount": winner_bid_amount,
        },
    )


@login_required
def bids(request):
    bids = Bid.objects.filter(bidder=request.user)
    winners = {}
    for bid in bids:
        listing = bid.listing
        winner, _ = get_winner(listing)
        if winner:
            winners[listing.id] = winner
    print(f"Winners: {winners}")
    return render(request, "auctions/bids.html", {"bids": bids, "winners": winners})
