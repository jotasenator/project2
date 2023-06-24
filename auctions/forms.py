from django import forms
from .models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            "title",
            "description",
            "starting_bid",
            "image_url",
            "category",
            "deadline",
        ]
        widgets = {
            "starting_bid": forms.NumberInput(attrs={"min": 0, "step": 0.01}),
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def save(self, commit=True):
        listing = super().save(commit=False)
        listing.title = listing.title.capitalize()
        listing.category = listing.category.capitalize()
        listing.description = listing.description.capitalize()
        if commit:
            listing.save()
        return listing
