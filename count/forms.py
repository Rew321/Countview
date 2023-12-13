from django import forms
from django.forms import ModelForm
from .models import*

modes = (
    ("driving", "driving"),
    ("walking", "walking"),
    ("bicycling", "bicycling"),
    ("transit", "transit")
)
class DistanceForm(ModelForm):
    from_location = forms.ModelChoiceField(label="Location from", required=True, queryset=Counter.objects.all())
    to_location = forms.ModelChoiceField(label="Location to", required=True, queryset=Counter.objects.all())
    mode = forms.ChoiceField(choices=modes, required=True)
    class Meta:
        model = Distance
        exclude = ['created_at', 'edited_at', 'distance_km', 'duration_traffic_min', 'distance_km', 'duration_min']