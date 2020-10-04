from django.contrib import admin

# Register your models here.
from .models import Tweet

class TweetAdmin(admin.ModelAdmin):
    list_display = ["__str__","user"] #The str method here is the default str method of the model. Can be changed
    search_fields = ["user__username","user__email","content"]
    class Meta:
        model = Tweet

admin.site.register(Tweet,TweetAdmin)