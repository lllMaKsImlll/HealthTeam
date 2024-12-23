from django.contrib import admin
from .models import *

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Record)
admin.site.register(Appointment)
admin.site.register(DoctorSchedule)
admin.site.register(Question)

class NewsAdmin(admin.ModelAdmin):
    exclude = ('date',)

admin.site.register(News, NewsAdmin)

@admin.register(HomeVisit)
class HomeVisitAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'address', 'scheduled_time', 'doctor', 'status')
    list_filter = ('status', 'doctor')
    search_fields = ('patient_name', 'address', 'doctor__fio')