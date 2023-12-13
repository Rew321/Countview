from django.shortcuts import redirect, render
from django.views import View

from count.forms import DistanceForm
from .models import Counter, Distance, Ipmodel
from django.views.generic import ListView, DetailView
from django.conf import settings
import googlemaps
from datetime import datetime

# Create your views here.
class indexView(ListView):
    model = Counter
    template_name = 'index.html'
    queryset = Counter.objects.all()
    context_object_name = 'counter'


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
class EventDetailView(DetailView):
    model = Counter
    context_object_name = 'counter'
    template_name = 'detail.html'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        ip = get_client_ip(self.request)
        print(ip)
        if Ipmodel.objects.filter(ip=ip).exists():
            print("Ip already present")
            post_id = request.GET.get('post-id')
            print(post_id)
            counter = Counter.objects.get(pk = post_id)
            counter.views.add(Ipmodel.objects.get(ip=ip))
            
        else:
            Ipmodel.objects.create(ip=ip)
            post_id = request.GET.get('post-id')
            counter = Counter.objects.get(pk = post_id)
            counter.views.add(Ipmodel.objects.get(ip=ip)) 
        return self.render_to_response(context)
    

class GeocodingView(View):
    template_name = 'geocoding.html'  
 
    
    def get(self, request, pk):
        location = Counter.objects.get(pk=pk)
        
        if location.lng and location.lat and location.place_id != None:
            
            lat = location.lat
            lng = location.lng
            place_id = location.place_id
            label = "from my database"
        
        elif location.name and location.description and location.date:
           name_string = str(location.name)+', '+str(location.description)+', '+str(location.date)
          
           gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
           result = gmaps.geocode(name_string)[0]
           
           lat = result.get('geometry', {}).get('location', {}).get('lat')
           lng = result.get('geometry', {}).get('location', {}).get('lng')
           place_id = result.get('place_id', ())
           label = "from my api call"
           
           location.lat = lat
           location.lng = lng
           location.place_id = place_id
           location.save()
           
        else:
            result = ""
            lat = ""
            lng = ""
            place_id = ""
            label = "no call made"
           
               
        context = {
            'location': location,
            'lat': lat,
            'lng': lng,
            'place_id': place_id,
            'label': label
        }
        
        return render(request, self.template_name, context)
                 
           
class DistanceView(View):
    template_name = 'distance.html'
    
    def get(self, request):
        form = DistanceForm()
        distance = Distance.objects.all()
        context = {
            'form': form,
            'distance': distance
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = DistanceForm(request.POST)
        if form.is_valid():
           from_location = form.cleaned_data['from_location']
           from_location_info = Counter.objects.get(name = from_location)
           from_name_string = str(from_location_info.name)+', '+str(from_location_info.description)+', '+str(from_location_info.date)
           
           to_location = form.cleaned_data['to_location']
           to_location_info = Counter.objects.get(name = to_location)
           to_name_string = str(to_location_info.name)+', '+str(to_location_info.description)+', '+str(to_location_info.date)
           
           mode = form.cleaned_data['mode']
           now  = datetime.now()
           gmaps = googlemaps.Client(key = settings.GOOGLE_API_KEY)
           calculate = gmaps.distance_matrix(
               from_name_string, 
               to_name_string, 
               mode = mode,
               departure_time=now
           )
           print (calculate)
        else:
            print(form.errors)    
        return redirect('my_distance_view')