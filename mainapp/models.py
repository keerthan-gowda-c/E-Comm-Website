from django.db import models

# Create your models here.
class CarouselImage(models.Model):
    image = models.ImageField(upload_to = 'carousel/')
    title = models.CharField(max_length = 200)
    caption = models.TextField(max_length = 300)
    added_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)
    is_active = models.BooleanField(default = True)


    def __str__(self):
        return f"Carousel - {self.title.capitalize()}"



