from django.db import models

# Create your models here.
class Ipmodel(models.Model):
    ip = models.CharField(max_length=100)
    def __str__(self):
        return self.ip

class Counter(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    date= models.DateTimeField(auto_now_add=True)
    views = models.ManyToManyField(Ipmodel, related_name='post_views', blank=True)
    
    lat = models.CharField(max_length=300, blank=True, null=True)
    lng = models.CharField(max_length=300, blank=True, null=True)
    place_id = models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
        return self.name
    
    def total_views(self):
        return self.views.count()
    
class Distance (models.Model):
   from_location = models.ForeignKey(Counter, on_delete=models.CASCADE, related_name='from_location')
   to_location = models.ForeignKey(Counter, on_delete=models.CASCADE, related_name='to_location')
   model = models.CharField(max_length=200, blank=True, null=True)
   distance_km = models.DecimalField(max_digits=10, decimal_places=2)
   duration_min = models.DecimalField(max_digits=10, decimal_places=2)
   duration_traffic_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
   created_at = models.DateTimeField(auto_now_add=True)
   edited_at = models.DateTimeField(auto_now=True)
   
   def __str__(self):
       return self.id