from django.contrib import admin
# Register your models here.
from django.contrib import admin
from pulseapp.models import sampledata,wwmeasure,trends,variantType,variants,covtype,uwtp,site,polygon

admin.site.register(sampledata)
admin.site.register(wwmeasure)
admin.site.register(trends)
admin.site.register(variantType)
admin.site.register(variants)
admin.site.register(covtype)
admin.site.register(uwtp)
admin.site.register(site)
admin.site.register(polygon)