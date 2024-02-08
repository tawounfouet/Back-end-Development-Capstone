from django.contrib import admin

# Register your models here.
from .models import Concert
from .models import ConcertAttending
# from .models import Photo
# from .models import Song


admin.site.register(Concert)
admin.site.register(ConcertAttending)
#admin.site.register(Photo)
#admin.site.register(Song)



